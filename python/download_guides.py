import requests
import os

GUIDES_DIR = "guides"
GUIDE_URLS = [
    "https://cs108.epfl.ch/g/group-work.html",
    "https://cs108.epfl.ch/g/sync.html",
    "https://cs108.epfl.ch/g/javadoc.html",
    "https://cs108.epfl.ch/g/style.html",
    "https://cs108.epfl.ch/g/how-to-debug.html"
]

def download_guide(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Extract filename from URL
            filename = url.split('/')[-1]
            filepath = os.path.join(GUIDES_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Downloaded guide: {filename}")
            return True
        else:
            print(f"Failed to download guide {url} (status code: {response.status_code})")
            return False
    except Exception as e:
        print(f"Error downloading guide {url}: {e}")
        return False

def main():
    for url in GUIDE_URLS:
        download_guide(url)

if __name__ == "__main__":
    main()
