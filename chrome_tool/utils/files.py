import os
from pathlib import Path
from typing import List


def get_py_files(folder_path: Path) -> list[Path]:
    py_files: List[Path] = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                full_path = Path(root) / file
                py_files.append(full_path)
    return py_files

def ensure_init_py(file_path: Path) -> None:
    folder = file_path.resolve()
    (folder / "__init__.py").touch(exist_ok=True)
        
if __name__ == "__main__":
    home_path = Path.home()
    python_files = get_py_files(home_path)
    for file in python_files:
        print(file)
