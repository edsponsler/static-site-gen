from sys import argv
from copystatic import recurse_copy
from generate_site import generate_pages

# main.py is executed by the main.sh script in the project root directory
dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"

def main() -> None:
    basepath = "/"
    # handle command line argument for basepath
    if len(argv) == 2:
        basepath = argv[1]
    elif len(argv) > 2:
        raise ValueError("Usage: python src/main.py <basepath>")

    recurse_copy(dir_path_static, dir_path_public)
    generate_pages(dir_path_content, dir_path_public, "./template.html", basepath)

if __name__ == "__main__":
    main()
