from dataclasses import dataclass, field
from enum import Enum, auto

from pathlib import Path

class TreeMethods(Enum):
    RECURSIVE = auto()
    IGNORE_FOLDERS = auto()

    JUST_FOLDERS = auto()
    JUST_FILES = auto()

    ONLY_VISIBLE = auto() # modo pro vscode

@dataclass
class Folder:
    path: Path

    def __post_init__(self):
        if not self.path.is_dir():
            raise RuntimeError(f"Invalid path: {self.path}")

    files: list[Path] = field(default_factory = list)
    subfolders: list[Folder] = field(default_factory = list)

    def scan(self):
        self.files.clear()
        self.subfolders.clear()

        for item in self.path.iterdir():
            if item.is_dir():
                self.subfolders.append(Folder(item).scan())

            elif item.is_file():
                self.files.append(item)

            else:
                # ver caso especial depois
                continue

        return self

    def children(self):
        def sort_by_name(item: Path | Folder):
            name = item.name if isinstance(item, Path) else item.path.name
            return name.casefold()
            

        return sorted(self.files + self.subfolders, key = sort_by_name)
