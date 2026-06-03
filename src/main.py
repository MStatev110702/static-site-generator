from copystatic import copy_static_to_dest
from generate import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    #text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(text_node)
    copy_static_to_dest(dir_path_static, dir_path_public)
    generate_pages_recursive("./content", "./template.html", "./public")


if __name__ == '__main__':
    main()