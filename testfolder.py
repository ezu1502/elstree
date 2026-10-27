
from pathlib import Path

root = Path("tree_test")

files = [
    "main.py",
    "README.md",
    "program.exe",
    "script.pyc",
    ".venv/pyvenv.cfg",
    "src/app.py",
    "src/__pycache__/app.pyc",
    "src/program.exe",
    "src/cavalo/main.py",
    "src/cavalo/README.md",
    "src/utils.py",
    "tests/test_main.py",
    "tests/__pycache__/test_main.pyc",
    "assets/logo.png",
    "docs/README.md",
]

settings = '''{
    "files.exclude": {
        ".venv": true,
        "**/*.exe": true,
        "**/cavalo": true,
        "**/*.pyc": true,
        "**/__pycache__": true,
    }
}'''

for relative_path in files:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"Arquivo de teste: {relative_path}\\n", encoding="utf-8")

settings_path = root / ".vscode" / "settings.json"
settings_path.parent.mkdir(parents=True, exist_ok=True)
settings_path.write_text(settings, encoding="utf-8")

print(f"Árvore de teste criada em: {root.resolve()}")
