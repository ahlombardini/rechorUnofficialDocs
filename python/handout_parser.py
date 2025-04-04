from bs4 import BeautifulSoup
import os
import re
import html

class HandoutParser:
    def __init__(self, handouts_dir, summaries_dir):
        self.handouts_dir = handouts_dir
        self.summaries_dir = summaries_dir
        self.classes_dir = os.path.join(summaries_dir, 'classes')

        # Create classes directory if it doesn't exist
        if not os.path.exists(self.classes_dir):
            os.makedirs(self.classes_dir)
        else:
            # Clean up existing class files
            for file in os.listdir(self.classes_dir):
                if file.endswith('.html'):
                    os.remove(os.path.join(self.classes_dir, file))

    def generate_class_page(self, class_div, handout_num, class_name):
        """Generate a dedicated HTML page for a class section"""
        html = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>{class_name} - Handout {handout_num}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 2em; line-height: 1.6; }}
                .class-section {{
                    margin: 2em 0;
                    padding: 1.5em;
                    background: #f5f5f5;
                    border-left: 4px solid #4CAF50;
                    border-radius: 3px;
                }}
                .method-block {{
                    margin: 1em 0;
                    padding: 1em;
                    background: white;
                    border: 1px solid #ddd;
                    border-radius: 3px;
                }}
                .tip-block {{
                    margin: 1em 0;
                    padding: 1em;
                    background: #fffaf0;
                    border-left: 4px solid #FFA500;
                    border-radius: 3px;
                }}
                .code-block {{
                    margin: 1em 0;
                    padding: 1em;
                    background: #f8f8f8;
                    border: 1px solid #ddd;
                    border-radius: 3px;
                    font-family: monospace;
                }}
                pre {{ white-space: pre-wrap; margin: 0; }}
                h1 {{ color: #1976D2; }}
                h2 {{ color: #2196F3; }}
                h3 {{ color: #4CAF50; }}
                h4 {{ color: #FF9800; }}
                .back-link {{
                    display: inline-block;
                    margin-bottom: 1em;
                    padding: 0.5em 1em;
                    color: #1976D2;
                    text-decoration: none;
                    border: 1px solid #1976D2;
                    border-radius: 3px;
                }}
                .back-link:hover {{
                    background: #1976D2;
                    color: white;
                }}
                table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f5f5f5; }}
                ul, ol {{ padding-left: 2em; }}
                dl {{ margin: 1em 0; }}
                dt {{ font-weight: bold; margin-top: 0.5em; }}
                dd {{ margin-left: 2em; }}
                code {{ background: #f5f5f5; padding: 0.2em 0.4em; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <a href="../summary_{handout_num}.html" class="back-link">← Retour au handout</a>
            {str(class_div)}
        </body>
        </html>
        """
        return html

    def parse_and_reformat(self, filename):
        """Parse a handout file and reformat it to highlight classes and tips"""
        handout_num = filename.split('.')[0].split('_')[-1]  # Extract number from handout_XX.html

        with open(os.path.join(self.handouts_dir, filename), 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')

            # Create new HTML structure
            new_soup = BeautifulSoup("""
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <title></title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 2em; line-height: 1.6; }
                    header { margin-bottom: 2em; }
                    .section {
                        margin: 1.5em 0;
                        padding: 1em;
                        background: #f8f9fa;
                        border-radius: 3px;
                        border: 1px solid #dee2e6;
                    }
                    .subsection {
                        margin: 1em 0;
                        padding: 1em;
                        background: #fff;
                        border-left: 3px solid #2196F3;
                    }
                    .class-section {
                        margin: 2em 0;
                        padding: 1.5em;
                        background: #f5f5f5;
                        border-left: 4px solid #4CAF50;
                        border-radius: 3px;
                        cursor: pointer;
                        transition: all 0.2s ease;
                    }
                    .class-section:hover {
                        transform: translateX(5px);
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    }
                    .method-block {
                        margin: 1em 0;
                        padding: 1em;
                        background: white;
                        border: 1px solid #ddd;
                        border-radius: 3px;
                    }
                    .tip-block {
                        margin: 1em 0;
                        padding: 1em;
                        background: #fffaf0;
                        border-left: 4px solid #FFA500;
                        border-radius: 3px;
                    }
                    .code-block {
                        margin: 1em 0;
                        padding: 1em;
                        background: #f8f8f8;
                        border: 1px solid #ddd;
                        border-radius: 3px;
                        font-family: monospace;
                    }
                    .section-dropdown {
                        margin: 2em 0;
                        border: 1px solid #ddd;
                        border-radius: 3px;
                    }
                    .section-header {
                        padding: 1em;
                        background: #f8f9fa;
                        cursor: pointer;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }
                    .section-header:hover {
                        background: #e9ecef;
                    }
                    .section-header::after {
                        content: '▼';
                        font-size: 0.8em;
                        transition: transform 0.3s ease;
                    }
                    .section-header.collapsed::after {
                        transform: rotate(-90deg);
                    }
                    .section-content {
                        padding: 1em;
                        display: none;
                    }
                    .section-content.expanded {
                        display: block;
                    }
                    pre { white-space: pre-wrap; margin: 0; }
                    h1 { color: #1976D2; margin-bottom: 0.5em; }
                    h2 { color: #2196F3; margin: 0; }
                    h3 { color: #4CAF50; }
                    h4 { color: #FF9800; }
                    .class-link {
                        text-decoration: none;
                        color: inherit;
                        display: block;
                    }
                    .class-link:hover {
                        color: inherit;
                    }
                    table { border-collapse: collapse; width: 100%; margin: 1em 0; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f5f5f5; }
                    ul, ol { padding-left: 2em; }
                    dl { margin: 1em 0; }
                    dt { font-weight: bold; margin-top: 0.5em; }
                    dd { margin-left: 2em; }
                    code { background: #f5f5f5; padding: 0.2em 0.4em; border-radius: 3px; }
                </style>
                <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        document.querySelectorAll('.section-header').forEach(header => {
                            header.addEventListener('click', function() {
                                const content = this.nextElementSibling;
                                const isExpanded = content.classList.contains('expanded');

                                // Toggle current section
                                content.classList.toggle('expanded');
                                this.classList.toggle('collapsed');

                                // Save state
                                const sectionId = this.parentElement.id;
                                const expandedSections = JSON.parse(localStorage.getItem('expandedSections') || '{}');
                                expandedSections[sectionId] = !isExpanded;
                                localStorage.setItem('expandedSections', JSON.stringify(expandedSections));
                            });
                        });

                        // Restore state
                        const expandedSections = JSON.parse(localStorage.getItem('expandedSections') || '{}');
                        Object.entries(expandedSections).forEach(([sectionId, isExpanded]) => {
                            if (isExpanded) {
                                const section = document.getElementById(sectionId);
                                if (section) {
                                    section.querySelector('.section-content').classList.add('expanded');
                                    section.querySelector('.section-header').classList.remove('collapsed');
                                }
                            }
                        });
                    });
                </script>
            </head>
            <body>
            </body>
            </html>
            """, 'html.parser')

            # Copy title and subtitle into header
            header = new_soup.new_tag('header')
            title = soup.find('h1', class_='title')
            subtitle = soup.find('p', class_='subtitle')
            if title:
                new_soup.head.title.string = title.get_text()
                header.append(title)
            if subtitle:
                header.append(subtitle)
            new_soup.body.append(header)

            # Process all main sections
            for section in soup.find_all('div', class_='outline-2'):
                section_num = section.find('h2')
                if section_num:
                    section_text = section_num.get_text().strip()
                    section_id = section.get('id', '')

                    # Create section container
                    section_div = new_soup.new_tag('div', attrs={'class': 'section', 'id': section_id})

                    # Create section header
                    section_header = new_soup.new_tag('div', attrs={'class': 'section-header collapsed'})
                    section_header.append(section_num)
                    section_div.append(section_header)

                    # Create section content
                    section_content = new_soup.new_tag('div', attrs={'class': 'section-content'})

                    # Copy section introduction text if any
                    intro_div = section.find('div', class_='outline-text-2')
                    if intro_div:
                        for elem in intro_div.contents:
                            if isinstance(elem, str):
                                new_p = new_soup.new_tag('p')
                                new_p.string = elem
                                section_content.append(new_p)
                            else:
                                section_content.append(elem)

                    # Process subsections
                    for subsection in section.find_all(['div', 'h3', 'h4'], class_=['outline-3', 'outline-4']):
                        if subsection.name in ['h3', 'h4']:
                            section_content.append(subsection)
                        else:
                            header = subsection.find(['h3', 'h4'])
                            if header:
                                section_text = header.get_text().strip()
                                # Look for class sections
                                match = re.match(r'(\d+\.\d+)\.\s*(.*)', section_text)

                                if match:
                                    section_title = match.group(2)
                                    is_class_section = any(keyword in section_title for keyword in
                                        ['Classe', 'Interface', 'Enregistrement', 'Classes'])

                                    if is_class_section:
                                        # Extract class name
                                        class_name = None
                                        for keyword in ['Classe', 'Interface', 'Enregistrement', 'Classes']:
                                            if keyword in section_title:
                                                class_name = section_title.split(keyword)[-1].strip()
                                                break

                                        if class_name:
                                            # Create class section
                                            class_div = new_soup.new_tag('div', attrs={'class': 'class-section'})
                                            class_div.append(header)

                                            # Copy content
                                            content_div = subsection.find('div', class_=re.compile(r'outline-text-[34]'))
                                            if content_div:
                                                for elem in content_div.contents:
                                                    if isinstance(elem, str):
                                                        new_p = new_soup.new_tag('p')
                                                        new_p.string = elem
                                                        class_div.append(new_p)
                                                    else:
                                                        if elem.name == 'pre':
                                                            code_div = new_soup.new_tag('div', attrs={'class': 'code-block'})
                                                            elem.wrap(code_div)
                                                            class_div.append(code_div)
                                                        elif isinstance(elem, str) and 'conseil' in elem.lower():
                                                            tip_div = new_soup.new_tag('div', attrs={'class': 'tip-block'})
                                                            new_p = new_soup.new_tag('p')
                                                            new_p.string = elem
                                                            tip_div.append(new_p)
                                                            class_div.append(tip_div)
                                                        else:
                                                            class_div.append(elem)

                                            # Create class page
                                            class_page = self.generate_class_page(class_div, handout_num, class_name)
                                            class_filename = f'class_{handout_num}_{class_name.lower().replace(".", "_")}.html'
                                            with open(os.path.join(self.classes_dir, class_filename), 'w', encoding='utf-8') as f:
                                                f.write(class_page)

                                            # Add class link to section
                                            class_link = new_soup.new_tag('a', href=f'classes/{class_filename}', attrs={'class': 'class-link'})
                                            class_link.append(class_div)
                                            section_content.append(class_link)
                                    else:
                                        # Create regular subsection
                                        subsection_div = new_soup.new_tag('div', attrs={'class': 'subsection'})
                                        subsection_div.append(header)

                                        content_div = subsection.find('div', class_=re.compile(r'outline-text-[34]'))
                                        if content_div:
                                            for elem in content_div.contents:
                                                if isinstance(elem, str):
                                                    new_p = new_soup.new_tag('p')
                                                    new_p.string = elem
                                                    subsection_div.append(new_p)
                                                else:
                                                    subsection_div.append(elem)

                                        section_content.append(subsection_div)

                    section_div.append(section_content)
                    new_soup.body.append(section_div)

            # Save the reformatted file
            with open(os.path.join(self.summaries_dir, f'summary_{handout_num}.html'), 'w', encoding='utf-8') as f:
                f.write(str(new_soup))

def main():
    handouts_dir = 'handouts'
    summaries_dir = 'summaries'
    parser = HandoutParser(handouts_dir, summaries_dir)

    # Process each handout file
    for filename in os.listdir(handouts_dir):
        if filename.endswith('.html'):
            print(f"Reformatting {filename}...")
            parser.parse_and_reformat(filename)

if __name__ == '__main__':
    main()
