import shutil
from pathlib import Path

def create_unofficial_doc():
    """Create unofficialDoc directory with only documentation files."""
    # Define source and target directories
    root_dir = Path('.')
    target_dir = root_dir / 'unofficialDoc'

    # Create target directory
    target_dir.mkdir(exist_ok=True)

    # Copy directories
    dirs_to_copy = ['handouts', 'guides', 'summaries']
    for dir_name in dirs_to_copy:
        src_dir = root_dir / dir_name
        if src_dir.exists():
            dst_dir = target_dir / dir_name
            if dst_dir.exists():
                shutil.rmtree(dst_dir)
            shutil.copytree(src_dir, dst_dir)
            print(f"Copied {dir_name}/")

    # Copy Python files
    for py_file in root_dir.glob('*.py'):
        shutil.copy2(py_file, target_dir)
        print(f"Copied {py_file.name}")

if __name__ == '__main__':
    create_unofficial_doc()
