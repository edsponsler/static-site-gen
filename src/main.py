from copystatic import recurse_copy
from generate_site import generate_page

# main.py is executed by the main.sh script in the project root directory
dir_path_static = "./static"
dir_path_public = "./public"

def main() -> None:
    recurse_copy(dir_path_static, dir_path_public)
    generate_page("./content/index.md", "./public/index.html", "./template.html")

if __name__ == "__main__":
    main()
