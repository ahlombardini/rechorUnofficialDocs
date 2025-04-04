from bs4 import BeautifulSoup
from extractparts import extractIntro, extractConcepts, extractImplementation

def test_extraction(handout_path):
    """Test the extraction functions on a given handout file."""
    with open(handout_path, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')

        print("Testing Introduction Extraction:")
        intro = extractIntro(soup)
        if intro:
            print(f"Title: {intro['title']}")
            print(f"Subtitle: {intro['subtitle']}")
            print("Introduction content found")
        else:
            print("No introduction found")

        print("\nTesting Concepts Extraction:")
        concepts = extractConcepts(soup)
        if concepts:
            print(f"Header: {concepts['header']}")
            print(f"Number of subsections: {len(concepts['subsections'])}")
            for i, sub in enumerate(concepts['subsections'], 1):
                print(f"  {i}. {sub['header']}")
        else:
            print("No concepts section found")

        print("\nTesting Implementation Extraction:")
        impl = extractImplementation(soup)
        if impl:
            print(f"Header: {impl['header']}")
            print(f"Number of classes: {len(impl['classes'])}")
            for i, cls in enumerate(impl['classes'], 1):
                print(f"  {i}. Class: {cls['name']}")
            print(f"Number of other subsections: {len(impl['other_subsections'])}")
        else:
            print("No implementation section found")

if __name__ == '__main__':
    test_extraction('handouts/handout_03.html')
