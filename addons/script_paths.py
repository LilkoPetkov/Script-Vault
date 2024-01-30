import os

from pathlib import Path

# Get the app root
app_root = Path(__file__).parents[1]


# Find the script
def find_script(name: str, path: str) -> str:
    for root, _, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


# Return the script
def get_script(script_name: str) -> str:
    script_path = find_script(name=script_name, path=app_root)

    if script_path:
        return os.path.join(app_root, script_path)
    return "No file found"


# Find scripts folder

# Find the script
def find_script_folder(name: str = "scripts", path: str = app_root) -> str:
    for root, folder, _ in os.walk(path):
        if name in folder:
            return os.path.join(root, name)
