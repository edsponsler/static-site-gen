from copystatic import recurse_copy
from generate_site import generate_pages

# main.py is executed by the main.sh script in the project root directory
dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"

def main() -> None:
    recurse_copy(dir_path_static, dir_path_public)
    generate_pages(dir_path_content, dir_path_public, "./template.html")

if __name__ == "__main__":
    main()
