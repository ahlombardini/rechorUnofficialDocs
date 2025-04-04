from bs4 import BeautifulSoup
from extractparts import extractIntro, extractConcepts, extractImplementation
import os
import json
from pathlib import Path

def process_handout(handout_path):
    """Process a single handout file and extract its parts."""
    print(f"\nProcessing {handout_path}...")

    with open(handout_path, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')

        # Extract all parts
        intro = extractIntro(soup)
        concepts = extractConcepts(soup)
        implementation = extractImplementation(soup)

        # Create the output structure
        result = {
            'intro': {
                'title': intro['title'] if intro else None,
                'subtitle': intro['subtitle'] if intro else None,
                'content': str(intro['content']) if intro and intro.get('content') else None
            },
            'concepts': {
                'header': concepts['header'] if concepts else None,
                'subsections': [
                    {
                        'header': sub['header'],
                        'content': str(sub['content'])
                    }
                    for sub in (concepts['subsections'] if concepts else [])
                ]
            },
            'implementation': {
                'header': implementation['header'] if implementation else None,
                'classes': [
                    {
                        'name': cls['name'],
                        'header': cls['header'],
                        'content': str(cls['content'])
                    }
                    for cls in (implementation['classes'] if implementation else [])
                ],
                'other_subsections': [
                    {
                        'header': sub['header'],
                        'content': str(sub['content'])
                    }
                    for sub in (implementation['other_subsections'] if implementation else [])
                ]
            }
        }

        return result

def save_extracted_parts(handout_number, parts):
    """Save the extracted parts to appropriate files."""
    # Create output directories if they don't exist
    output_dir = Path('../summaries/extracted')
    output_dir.mkdir(exist_ok=True)

    # Save the full extraction result as JSON
    output_file = output_dir / f'handout_{handout_number:02d}_parts.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parts, f, ensure_ascii=False, indent=2)

    # Create HTML files for each class in the implementation
    classes_dir = Path('../summaries/classes')
    classes_dir.mkdir(exist_ok=True)

    if parts['implementation']['classes']:
        for cls in parts['implementation']['classes']:
            class_name = cls['name'].strip()
            if class_name:
                class_file = classes_dir / f'{class_name}.html'
                with open(class_file, 'w', encoding='utf-8') as f:
                    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8"/>
    <title>{class_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2em; line-height: 1.6; }}
        .class-content {{ margin: 2em 0; padding: 1.5em; background: #f5f5f5; border-left: 4px solid #4CAF50; }}
        pre {{ white-space: pre-wrap; margin: 0; background: #f8f8f8; padding: 1em; }}
        h1 {{ color: #1976D2; }}
        h2 {{ color: #2196F3; }}
    </style>
</head>
<body>
    <h1>{class_name}</h1>
    <h2>{cls['header']}</h2>
    <div class="class-content">
        {cls['content']}
    </div>
</body>
</html>"""
                    f.write(html_content)

def main():
    """Process all handout files."""
    handouts_dir = Path('handouts')

    # Process each handout file
    for handout_file in sorted(handouts_dir.glob('handout_*.html')):
        # Extract handout number from filename
        handout_num = int(handout_file.stem.split('_')[1])

        # Process the handout
        parts = process_handout(handout_file)

        # Save the extracted parts
        save_extracted_parts(handout_num, parts)

        print(f"✓ Processed handout_{handout_num:02d}.html")
        if parts['implementation']['classes']:
            print(f"  Found {len(parts['implementation']['classes'])} classes/interfaces")
            for cls in parts['implementation']['classes']:
                print(f"    - {cls['name']}")

if __name__ == '__main__':
    main()
