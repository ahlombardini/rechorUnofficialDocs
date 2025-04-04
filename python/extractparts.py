from bs4 import BeautifulSoup
import re

def extractIntro(soup):
    """
    Extract the introduction section from the handout.
    Returns a tuple containing (title, subtitle, intro_content).
    """
    # Get title and subtitle
    title = soup.find('h1', class_='title')
    subtitle = soup.find('p', class_='subtitle')

    # Find the first outline-2 div with id starting with 'outline-container'
    intro_section = soup.find('div', id=lambda x: x and x.startswith('outline-container-org'))
    if intro_section:
        # Get the content div
        content = intro_section.find('div', class_='outline-text-2')
        if content:
            return {
                'title': title.get_text() if title else None,
                'subtitle': subtitle.get_text() if subtitle else None,
                'content': content
            }
    return None

def extractConcepts(soup):
    """
    Extract the concepts section from the handout.
    Returns a dictionary containing the concepts section and its subsections.
    """
    # Find all outline-2 divs
    sections = soup.find_all('div', class_='outline-2')
    for section in sections:
        # Get the section number from any h3 tags within outline-3 divs
        subsections = section.find_all('div', class_='outline-3')
        if subsections:
            first_subsection = subsections[0]
            header = first_subsection.find('h3')
            if header and '2.' in header.get_text():
                # Get all subsections
                processed_subsections = []
                for subsection in subsections:
                    sub_header = subsection.find('h3')
                    content = subsection.find('div', class_='outline-text-3')
                    if sub_header and content:
                        processed_subsections.append({
                            'header': sub_header.get_text(),
                            'content': content
                        })

                return {
                    'header': header.get_text() if header else None,
                    'intro': section.find('div', class_='outline-text-2'),
                    'subsections': processed_subsections
                }
    return None

def extractImplementation(soup):
    """
    Extract the implementation section from the handout.
    Returns a dictionary containing the implementation section, its classes, and other subsections.
    """
    # Find all outline-2 divs
    sections = soup.find_all('div', class_='outline-2')
    for section in sections:
        # Get all subsections to check for section 3
        subsections = section.find_all('div', class_='outline-3')
        if subsections:
            first_subsection = subsections[0]
            header = first_subsection.find('h3')
            if header and '3.' in header.get_text():
                # Get all subsections
                classes = []
                other_subsections = []

                # Get introduction text
                intro = section.find('div', class_='outline-text-2')

                # Process all subsections
                for subsection in subsections:
                    sub_header = subsection.find('h3')
                    if sub_header:
                        section_text = sub_header.get_text().strip()
                        # Look for class sections
                        match = re.search(r'3\.\d+\.\s*(.*)', section_text)

                        if match:
                            section_title = match.group(1)
                            is_class_section = any(keyword in section_title.lower() for keyword in
                                ['classe', 'interface', 'enregistrement'])

                            content = subsection.find('div', class_='outline-text-3')

                            if is_class_section:
                                # Extract class name
                                class_name = section_title
                                for keyword in ['Classe', 'Interface', 'Enregistrement']:
                                    if keyword.lower() in section_title.lower():
                                        class_name = section_title.split(keyword)[-1].strip()
                                        break

                                if class_name:
                                    classes.append({
                                        'name': class_name,
                                        'header': sub_header.get_text(),
                                        'content': content
                                    })
                            else:
                                other_subsections.append({
                                    'header': sub_header.get_text(),
                                    'content': content
                                })

                return {
                    'header': header.get_text() if header else None,
                    'intro': intro,
                    'classes': classes,
                    'other_subsections': other_subsections
                }
    return None
