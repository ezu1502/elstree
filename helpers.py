import argparse
from pathlib import Path

from core import TreeMethods as TM, Folder

import json5


RAM = "├"
HORI = "─"
VERTI = "│"
RAM_LAST = "└"

def read_method(method_str) -> TM | None:
    match method_str:
        case "recursive":
            return TM.RECURSIVE
        case "ignore-folders":
            return TM.IGNORE_FOLDERS

        case "just-folders":
            return TM.JUST_FOLDERS
        case "just-files":
            return TM.JUST_FILES

        case "only-visible":
            return TM.ONLY_VISIBLE
        
        case _:
            return None


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = "Print a directory tree."
    )

    parser.add_argument(
        "folder",
        nargs = "?",
        type = Path,
        default = Path.cwd()
    )

    parser.add_argument(
        "--method",
        "-m",

        choices=[
            "recursive",
            "ignore-folders",
            "just-folders",
            "just-files",
            "only-visible"
        ],
        default="recursive"
    )

    return parser.parse_args()


def generate_tree(folder: Folder, cwd: Path, *, indent: int = 4, method: TM = TM.RECURSIVE) -> str:
    exclude = []
    
    if method == TM.ONLY_VISIBLE:
        settings_path = Path(cwd/ ".vscode" / "settings.json")
        if not settings_path.is_file():
            return "settings.json not found!"
            
        settings_dict = json5.loads(settings_path.read_text(encoding = "utf-8"))
        
        exclude_dict = settings_dict.get("files.exclude", {})
    
        exclude = [item for item, hide in exclude_dict.items() if hide is True]

        keep_visibles(folder, cwd, exclude)
        
        
    def generate(dir: Folder, prefix: str = ""):
        result: list[str] = []
        
        if not prefix:
            result.append(dir.path.name + "/")

        

        children: list[Path | Folder] = dir.children()

        for indx, child in enumerate(children):
            connector = RAM_LAST if indx == len(children) - 1 else RAM
            if isinstance(child, Path):
                if method == TM.JUST_FOLDERS:
                    continue

                result.append(prefix + connector + HORI + " " + child.name)

            else:
                if method == TM.JUST_FILES:
                    continue

                tab: str = " " * indent
                result.append(prefix + connector + HORI + " " + child.path.name + "/")

                if method == TM.IGNORE_FOLDERS:
                    continue

                new_prefix: str = prefix + (tab if indx == len(children) - 1 else VERTI + tab)

                subtree: str = generate(child, prefix = new_prefix)

                if subtree:
                    result.append(subtree)

            

        return "\n".join(result)

    return generate(folder)


def keep_visibles(folder: Folder, cwd: Path, exclude: list):
    def remove_excluded(folder: Folder) -> None:
        for item in folder.children():
            if isinstance(item, Path):
                if any(item.resolve().relative_to(cwd.resolve()).full_match(pattern) for pattern in exclude):
                    folder.files.remove(item)
            elif isinstance(item, Folder):
                if any(item.path.resolve().relative_to(cwd.resolve()).full_match(pattern) for pattern in exclude):
                    folder.subfolders.remove(item)

        for item in folder.children():
            if not isinstance(item, Folder):
                continue
            
            remove_excluded(item)

    remove_excluded(folder)


