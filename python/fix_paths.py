import os
from pathlib import Path

def fix_file_paths(file_path):
    """Fix paths in a Python file to be relative to unofficialDoc."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Common path replacements
    replacements = {
        'handouts/': '../handouts/',
        'guides/': '../guides/',
        'summaries/': '../summaries/',
        "'./handouts'": "'../handouts'",
        "'./guides'": "'../guides'",
        "'./summaries'": "'../summaries'",
        'Path("handouts")': 'Path("../handouts")',
        'Path("guides")': 'Path("../guides")',
        'Path("summaries")': 'Path("../summaries")',
        'os.chdir(Path(__file__).parent / \'summaries\')': 'os.chdir(Path(__file__).parent.parent / \'summaries\')',
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """Update paths in all Python files."""
    python_dir = Path(__file__).parent

    # List of files to update
    files_to_update = [
        'download_guides.py',
        'download_handouts.py',
        'extractparts.py',
        'generate_static_docs.py',
        'handout_parser.py',
        'process_handouts.py',
        'serve_docs.py',
    ]

    for filename in files_to_update:
        file_path = python_dir / filename
        if file_path.exists():
            print(f"Fixing paths in {filename}...")
            fix_file_paths(file_path)
        else:
            print(f"Warning: {filename} not found")

if __name__ == '__main__':
    main()
    print("Path fixes completed!")
