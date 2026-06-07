from os import listdir, mkdir
from os.path import exists, join, isfile
from shutil import copy, rmtree

def recurse_copy(src_dir: str, dest_dir: str) -> None:
    if not exists(src_dir):
        raise FileNotFoundError(f"Source directory {src_dir} does not exist.")
    if exists(dest_dir):
        rmtree(dest_dir)
    mkdir(dest_dir)    
    
    for item in listdir(src_dir):
        src_path = join(src_dir, item)
        dest_path = join(dest_dir, item)

        if isfile(src_path):
            print(f"Copying {src_path} -> {dest_path}")
            copy(src_path, dest_path)
        else:
            print(f"Recursing {src_path} -> {dest_path}")
            recurse_copy(src_path, dest_path)
