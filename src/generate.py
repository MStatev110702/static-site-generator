import os
from markdown_blocks import markdown_to_html_node
from inline_markdown import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to  {dest_path} using {template_path}")
    
    from_file = open(from_path, "r")
    markdown = from_file.read()
    from_file.close()
    
    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown)
    html = node.to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    
    dest_dir_path = os.path.dirname(dest_path)
    
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    to_file = open(dest_path, "w")
    to_file.write(template)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content = os.listdir(dir_path_content)
    for item in content:
        full_path = os.path.join(dir_path_content, item)
        if not os.path.isfile(full_path):
            generate_pages_recursive(full_path, template_path, os.path.join(dest_dir_path, item))
            continue

        filename = os.path.splitext(item)[0] + ".html"
        dest_path = os.path.join(dest_dir_path, filename)
        generate_page(full_path, template_path, dest_path)