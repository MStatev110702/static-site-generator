import sys
from copystatic import copy_static_to_dest
from generate import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"

def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else ""
    if not base_path.strip():
        base_path = "/"
    copy_static_to_dest(dir_path_static, dir_path_public)
    generate_pages_recursive("./content", "./template.html", "./docs", base_path)


if __name__ == '__main__':
    main()