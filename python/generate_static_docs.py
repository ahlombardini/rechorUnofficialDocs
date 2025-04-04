import json
from pathlib import Path
import html
import re

def load_handout_data():
    """Load all handout data from JSON files."""
    handouts = []
    classes = {}  # Store all classes with their handout number
    for i in range(1, 8):  # Handouts 1-7
        file_path = Path(f'../summaries/extracted/handout_{i:02d}_parts.json')
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                handouts.append({
                    'number': i,
                    'data': data
                })
                # Collect classes from this handout
                if data.get('implementation') and data['implementation'].get('classes'):
                    for cls in data['implementation']['classes']:
                        # Only strip the section numbers (e.g., "3.1. ")
                        class_name = re.sub(r'^\d+\.\d+\.\s*', '', cls['name'])
                        classes[class_name] = {
                            'handout': i,
                            'data': {
                                **cls,
                                'name': class_name  # Update the name in the data too
                            },
                            'handout_title': data['intro']['title'] if data.get('intro') and data['intro'].get('title') else None
                        }
    return handouts, classes

def create_class_card_html(class_name, class_data):
    """Generate HTML for a class card."""
    header = html.escape(class_data.get('header', '')) if class_data.get('header') else ''
    content = class_data.get('content', '')
    return f"""
        <div class="class-card">
            <h3 class="card-title">
                <a href="classes/{class_name}.html">{html.escape(class_name)}</a>
            </h3>
            <div class="class-content">
                {content}
            </div>
        </div>
    """

def create_concept_card_html(concept):
    """Generate HTML for a concept card."""
    if not isinstance(concept, dict):
        return ''

    # Get the header and content from either direct concept or subsection
    header = concept.get('header', '')
    content = concept.get('content', '')

    # Remove the section numbers (e.g., "2.1. ") from the header
    header = re.sub(r'^\d+\.\d+\.\s*', '', header)
    header = html.escape(header)

    # Create a URL-friendly filename for the concept page link
    filename = header.lower().replace(' ', '_').replace('é', 'e').replace('è', 'e').replace('à', 'a')
    filename = re.sub(r'[^a-z0-9_-]', '', filename)

    # Create a preview by extracting text from the first paragraph
    preview_text = re.sub(r'<[^>]+>', '', content)
    preview_text = re.sub(r'\s+', ' ', preview_text).strip()
    if len(preview_text) > 100:
        preview_text = preview_text[:97] + '...'

    return f"""
        <div class="concept-card">
            <h3 class="card-title">
                <a href="../concepts/part{concept.get('part_number', '')}_{filename}.html">{header}</a>
            </h3>
            <div class="concept-preview">{preview_text}</div>
        </div>
    """

def create_project_part_html(handout, standalone=True):
    """Create HTML for a project part."""
    title = handout['data']['intro']['title'] if handout['data']['intro'] and handout['data']['intro'].get('title') else ''
    subtitle = handout['data']['intro']['subtitle'] if handout['data']['intro'] and handout['data']['intro'].get('subtitle') else ''
    intro_content = handout['data']['intro']['content'] if handout['data']['intro'] and handout['data']['intro'].get('content') else ''

    # Base HTML structure for standalone pages
    if standalone:
        html_content = f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Étape {handout["number"]} - ReCHor Documentation</title>
    <style>
        :root {{
            --primary-color: #1976D2;
            --secondary-color: #2196F3;
            --accent-color: #4CAF50;
            --background-color: #f5f5f5;
            --text-color: #333;
        }}

        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: var(--text-color);
            background: var(--background-color);
        }}

        .header {{
            background: var(--primary-color);
            color: white;
            padding: 1rem 2rem;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
        }}

        .header a {{
            color: white;
            text-decoration: none;
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            transition: background-color 0.2s;
        }}

        .header a:hover {{
            background-color: rgba(255, 255, 255, 0.1);
            text-decoration: none;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        h2 {{
            color: var(--primary-color);
            margin-top: 0;
        }}

        .card-title {{
            word-wrap: break-word;
            overflow-wrap: break-word;
            hyphens: auto;
            margin: 0 0 1rem 0;
            color: var(--primary-color);
            font-size: 1.2rem;
        }}

        .class-card, .concept-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.2s ease-in-out;
            margin-bottom: 1rem;
        }}

        .class-card:hover, .concept-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}

        .card-title {{
            margin: 0 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #eee;
        }}

        .card-title a {{
            color: var(--primary-color);
            text-decoration: none;
            font-size: 1.2rem;
        }}

        .card-title a:hover {{
            color: var(--secondary-color);
        }}

        .class-content, .concept-content {{
            font-size: 0.95em;
            color: var(--text-color);
            overflow: auto;
            max-height: 500px;
            padding-right: 1rem;
        }}

        .class-content p, .concept-content p {{
            margin: 0.5rem 0;
        }}

        .class-content pre, .concept-content pre {{
            background: var(--background-color);
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
            margin: 1rem 0;
        }}

        .class-grid, .concept-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 1.5rem;
            margin: 1rem 0;
        }}

        .class-card .card-title {{
            margin: 0;
        }}

        .class-card, .concept-card {{
            min-height: 100px;
            height: fit-content;
            display: flex;
            flex-direction: column;
            background: white;
            padding: 1.5rem;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}

        .concept-card {{
            margin-bottom: 1rem;
        }}

        .concept-card:hover, .class-card:hover {{
            transform: translateY(-2px);
        }}

        .concept-content {{
            font-size: 0.95em;
            color: var(--text-color);
            overflow: auto;
            max-height: 300px;
            margin-top: 0.5rem;
        }}

        .concept-content p {{
            margin: 0.5rem 0;
        }}

        .concept-content ol, .concept-content ul {{
            margin: 0.5rem 0;
            padding-left: 1.5rem;
        }}

        .concept-content a {{
            color: var(--primary-color);
            text-decoration: none;
        }}

        .concept-content a:hover {{
            text-decoration: underline;
        }}

        .concepts-section {{
            margin: 2rem 0;
        }}

        .concepts-section h3 {{
            color: var(--primary-color);
            margin-bottom: 1rem;
        }}

        .class-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
            margin: 1rem 0;
        }}

        .class-card a {{
            text-decoration: none;
        }}

        .introduction {{
            background: white;
            padding: 2rem;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}

        .subtitle {{
            font-style: italic;
            color: var(--secondary-color);
            margin: 1rem 0;
        }}

        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 1rem auto;
        }}

        figure {{
            margin: 2rem 0;
            text-align: center;
        }}

        figcaption {{
            font-style: italic;
            color: var(--text-color);
            margin-top: 0.5rem;
        }}

        .concept-preview {{
            color: var(--text-color);
            font-size: 0.9em;
            margin-top: 0.5rem;
            opacity: 0.8;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
        }}

        .concept-card {{
            min-height: 100px;
            height: fit-content;
            background: white;
            padding: 1.5rem;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.2s ease-in-out;
        }}

        .concept-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}

        .concept-card a {{
            text-decoration: none;
            color: inherit;
            display: block;
            height: 100%;
        }}
    </style>
</head>
<body>
    <header class="header">
        <a href="../index.html">← Retour à l'index</a>
    </header>
    <div class="container">
        <h2>Étape {handout["number"]}{f' - {html.escape(title)}' if title else ''}</h2>
'''
        if subtitle:
            html_content += f'<p class="subtitle">{html.escape(subtitle)}</p>\n'
    else:
        html_content = ''

    # Add introduction content if it exists
    if intro_content:
        html_content += f'''
            <div class="introduction">
                {intro_content}
            </div>
        '''

    # Add concepts if they exist
    if handout['data'].get('concepts'):
        html_content += '''
                <div class="concepts-section">
                    <h3>Concepts clés</h3>
                    <div class="concept-grid">
            '''

        concepts = handout['data']['concepts']
        if isinstance(concepts, dict):
            # Handle concepts with subsections
            if concepts.get('subsections'):
                for subsection in concepts['subsections']:
                    if isinstance(subsection, dict):
                        subsection['part_number'] = handout['number']
                        html_content += create_concept_card_html(subsection)
            else:
                # If it's a direct concept without subsections
                concepts['part_number'] = handout['number']
                html_content += create_concept_card_html(concepts)
        elif isinstance(concepts, list):
            # Handle direct list of concepts
            for concept in concepts:
                if isinstance(concept, dict):
                    concept['part_number'] = handout['number']
                    html_content += create_concept_card_html(concept)

        html_content += '''
                    </div>
                </div>
        '''

    # Add classes if they exist
    if handout['data'].get('implementation') and handout['data']['implementation'].get('classes'):
        html_content += '''
                <div class="class-section">
                    <h3>Classes et Interfaces</h3>
                    <div class="class-grid">
        '''

        for cls in handout['data']['implementation']['classes']:
            # Only strip the section numbers (e.g., "3.1. ")
            class_name = re.sub(r'^\d+\.\d+\.\s*', '', cls['name'])
            html_content += create_class_card_html(class_name, cls)

        html_content += '''
                    </div>
                </div>
        '''

    if standalone:
        html_content += '''
    </div>
</body>
</html>
'''

    return html_content

def generate_class_page(class_name, class_info):
    """Generate an HTML page for a single class."""
    header = html.escape(class_info['data']['header']) if class_info['data'].get('header') else ''
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(class_name)} - ReCHor Documentation</title>
    <style>
        :root {{
            --primary-color: #1976D2;
            --secondary-color: #2196F3;
            --accent-color: #4CAF50;
            --background-color: #f5f5f5;
            --text-color: #333;
        }}

        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: var(--text-color);
        }}

        .header {{
            background: var(--primary-color);
            color: white;
            padding: 1rem 2rem;
        }}

        .header a {{
            color: white;
            text-decoration: none;
        }}

        .header a:hover {{
            text-decoration: underline;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .breadcrumb {{
            margin-bottom: 1rem;
            color: var(--secondary-color);
        }}

        .class-content {{
            background: white;
            padding: 2rem;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .class-header {{
            border-bottom: 2px solid var(--accent-color);
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }}

        .class-header h1 {{
            color: var(--primary-color);
            margin: 0;
        }}

        .class-header p {{
            color: var(--secondary-color);
            margin: 0.5rem 0 0 0;
        }}

        pre {{
            background: var(--background-color);
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
        }}

        .card-title {{
            word-wrap: break-word;
            overflow-wrap: break-word;
            hyphens: auto;
            margin: 0 0 1rem 0;
            color: var(--primary-color);
            font-size: 1.2rem;
        }}
    </style>
</head>
<body>
    <header class="header">
        <a href="../index.html">← Retour à l'index</a>
    </header>

    <div class="container">
        <div class="breadcrumb">
            <p>Étape {class_info['handout']}{f" - {html.escape(class_info['handout_title'])}" if class_info['handout_title'] else ""}</p>
        </div>

        <div class="class-content">
            <div class="class-header">
                <h1>{html.escape(class_name)}</h1>
                <p>{header}</p>
            </div>

            <div class="class-body">
                {class_info['data']['content']}
            </div>
        </div>
    </div>
</body>
</html>'''

def generate_concept_page(concept_name, concept_data):
    """Generate an HTML page for a single concept."""
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(concept_name)} - ReCHor Documentation</title>
    <style>
        :root {{
            --primary-color: #1976D2;
            --secondary-color: #2196F3;
            --accent-color: #4CAF50;
            --background-color: #f5f5f5;
            --text-color: #333;
        }}

        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: var(--text-color);
            background: var(--background-color);
        }}

        .header {{
            background: var(--primary-color);
            color: white;
            padding: 1rem 2rem;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
        }}

        .header a {{
            color: white;
            text-decoration: none;
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            transition: background-color 0.2s;
        }}

        .header a:hover {{
            background-color: rgba(255, 255, 255, 0.1);
            text-decoration: none;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .concept-content {{
            background: white;
            padding: 2rem;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}

        h1 {{
            color: var(--primary-color);
            margin-top: 0;
            margin-bottom: 2rem;
        }}

        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 1rem auto;
        }}

        figure {{
            margin: 2rem 0;
            text-align: center;
        }}

        figcaption {{
            font-style: italic;
            color: var(--text-color);
            margin-top: 0.5rem;
        }}

        .concept-content p {{
            margin: 1rem 0;
        }}

        .concept-content a {{
            color: var(--primary-color);
            text-decoration: none;
        }}

        .concept-content a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <header class="header">
        <a href="../index.html">← Retour à l'index</a>
    </header>
    <div class="container">
        <h1>{html.escape(concept_name)}</h1>
        <div class="concept-content">
            {concept_data['content']}
        </div>
    </div>
</body>
</html>'''

def generate_static_html():
    """Generate the complete static HTML file and class pages."""
    # Create directories if they don't exist
    Path('../docs').mkdir(parents=True, exist_ok=True)
    Path('../docs/classes').mkdir(parents=True, exist_ok=True)
    Path('../docs/parts').mkdir(parents=True, exist_ok=True)
    Path('../docs/concepts').mkdir(parents=True, exist_ok=True)

    # Load all handout data
    handouts, classes = load_handout_data()

    # Generate index page with links to parts
    index_content = '''
    <div class="container">
        <h1>Documentation ReCHor</h1>
        <div class="parts-list">
    '''

    for handout in handouts:
        title = handout['data']['intro']['title'] if handout['data']['intro'] and handout['data']['intro'].get('title') else ''
        index_content += f'''
            <div class="part-link">
                <a href="parts/part{handout['number']}.html">
                    Étape {handout['number']}{f' - {html.escape(title)}' if title else ''}
                </a>
            </div>
        '''

    index_content += '''
        </div>
    </div>
    '''

    # Add CSS for index page
    css_to_add = '''
        body {
            background: var(--background-color);
        }

        .parts-list {
            margin: 2rem 0;
        }

        .part-link {
            background: white;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }

        .part-link:hover {
            transform: translateY(-2px);
        }

        .part-link a {
            color: var(--primary-color);
            text-decoration: none;
            font-size: 1.2rem;
            display: block;
            width: 100%;
            height: 100%;
        }

        .part-link a:hover {
            text-decoration: none;
            color: var(--secondary-color);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        h1 {
            color: var(--primary-color);
            margin-bottom: 2rem;
        }
    '''

    # Create base template for index.html
    base_template = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation ReCHor</title>
    <style>
        :root {
            --primary-color: #1976D2;
            --secondary-color: #2196F3;
            --accent-color: #4CAF50;
            --background-color: #f5f5f5;
            --text-color: #333;
        }

        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: var(--text-color);
        }
        ''' + css_to_add + '''
    </style>
</head>
<body>
    ''' + index_content + '''
</body>
</html>
'''

    # Write the index.html to docs directory
    with open('../docs/index.html', 'w', encoding='utf-8') as f:
        f.write(base_template)

    # Generate individual part pages and concept pages
    for handout in handouts:
        # Generate part page
        part_html = create_project_part_html(handout, standalone=True)
        with open(f'../docs/parts/part{handout["number"]}.html', 'w', encoding='utf-8') as f:
            f.write(part_html)

        # Generate concept pages
        concepts = handout['data'].get('concepts', [])
        if isinstance(concepts, dict):
            # Handle subsections
            if concepts.get('subsections'):
                for concept in concepts['subsections']:
                    if isinstance(concept, dict) and concept.get('header'):
                        header = re.sub(r'^\d+\.\d+\.\s*', '', concept['header'])
                        filename = header.lower().replace(' ', '_').replace('é', 'e').replace('è', 'e').replace('à', 'a')
                        filename = re.sub(r'[^a-z0-9_-]', '', filename)
                        concept_html = generate_concept_page(header, concept)
                        with open(f'../docs/concepts/part{handout["number"]}_{filename}.html', 'w', encoding='utf-8') as f:
                            f.write(concept_html)
        elif isinstance(concepts, list):
            # Handle direct list of concepts
            for concept in concepts:
                if isinstance(concept, dict) and concept.get('header'):
                    header = re.sub(r'^\d+\.\d+\.\s*', '', concept['header'])
                    filename = header.lower().replace(' ', '_').replace('é', 'e').replace('è', 'e').replace('à', 'a')
                    filename = re.sub(r'[^a-z0-9_-]', '', filename)
                    concept_html = generate_concept_page(header, concept)
                    with open(f'../docs/concepts/part{handout["number"]}_{filename}.html', 'w', encoding='utf-8') as f:
                        f.write(concept_html)

    # Generate individual class pages
    for class_name, class_info in classes.items():
        class_html = generate_class_page(class_name, class_info)
        with open(f'../docs/classes/{class_name}.html', 'w', encoding='utf-8') as f:
            f.write(class_html)

    print(f"Generated documentation in docs/ directory: main index.html, {len(handouts)} part pages, and {len(classes)} class pages")

if __name__ == '__main__':
    generate_static_html()
