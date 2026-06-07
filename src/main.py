from copystatic import recurse_copy

# main.py is executed by the main.sh script in the project root directory
dir_path_static = "./static"
dir_path_public = "./public"

def main() -> None:
    recurse_copy(dir_path_static, dir_path_public)

if __name__ == "__main__":
    main()
