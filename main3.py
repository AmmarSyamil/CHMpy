from pathlib import Path


data =  {
    
}

def tree(dir):
    dir = Path(dir)
    if dir.name.startswith(".") or dir.name in {"__pycache__", ".venv", "venv", ".git", "myenv"}:
        return
    for subdir in dir.iterdir():
        print(subdir)
        if subdir.is_dir():
           tree(subdir)

tree('.')