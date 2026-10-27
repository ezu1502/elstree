import sys
from core import Folder
from helpers import read_method, get_args, generate_tree
from pathlib import Path

def main():
    args = get_args()

    if args is None:
        return 1

    folder_path, method = args.folder, read_method(args.method)

    if method is None or not folder_path.is_dir():
        return 1

    folder: Folder = Folder(folder_path).scan()
    

    print(generate_tree(folder, method = method, cwd = Path.cwd().resolve()))

    
# TODO terminar o instalador!


if __name__ == "__main__":
    sys.exit(main())