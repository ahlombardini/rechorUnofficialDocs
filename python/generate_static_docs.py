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
    return f"""
        <div class="class-card">
            <a href="classes/{class_name}.html">
                <h3 class="card-title">{html.escape(class_name)}</h3>
            </a>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9em;">{header}</p>
        </div>
    """

def create_concept_card_html(concept):
    """Generate HTML for a concept card."""
    # Remove the section numbers (e.g., "2.1. ") from the header
    header = re.sub(r'^\d+\.\d+\.\s*', '', concept['header'])
    header = html.escape(header)
    # Don't escape the content since it's already HTML
    content = concept.get('content', '')
    return f"""
        <div class="concept-card">
            <h3 class="card-title">{header}</h3>
            <div class="concept-content">{content}</div>
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

        .concept-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
            margin: 1rem 0;
            list-style: none;
            padding: 0;
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
            # Handle subsections
            for section in concepts.values():
                for concept in section:
                    html_content += create_concept_card_html(concept)
        elif isinstance(concepts, list):
            # Handle direct list of concepts
            for concept in concepts:
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

def generate_static_html():
    """Generate the complete static HTML file and class pages."""
    # Create directories if they don't exist
    Path('../summaries/classes').mkdir(parents=True, exist_ok=True)
    Path('../summaries/parts').mkdir(parents=True, exist_ok=True)

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

    # Write the index.html
    with open('../summaries/index.html', 'w', encoding='utf-8') as f:
        f.write(base_template)

    # Generate individual part pages
    for handout in handouts:
        part_html = create_project_part_html(handout, standalone=True)
        with open(f'../summaries/parts/part{handout["number"]}.html', 'w', encoding='utf-8') as f:
            f.write(part_html)

    # Generate individual class pages
    for class_name, class_info in classes.items():
        class_html = generate_class_page(class_name, class_info)
        with open(f'../summaries/classes/{class_name}.html', 'w', encoding='utf-8') as f:
            f.write(class_html)

    print(f"Generated main index.html, {len(handouts)} part pages, and {len(classes)} class pages")

if __name__ == '__main__':
    generate_static_html()
