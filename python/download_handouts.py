import requests
import os

BASE_URL = "https://cs108.epfl.ch/p/{:02d}.html"
HANDOUTS_DIR = "handouts"

def download_handout(number):
    url = BASE_URL.format(number)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(HANDOUTS_DIR, f"handout_{number:02d}.html")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Downloaded handout {number:02d}")
            return True
        else:
            print(f"Failed to download handout {number:02d} (status code: {response.status_code})")
            return False
    except Exception as e:
        print(f"Error downloading handout {number:02d}: {e}")
        return False

def main():
    # Try downloading handouts 1 through 20 (adjust range if needed)
    for i in range(1, 21):
        if not download_handout(i):
            # If we get two consecutive failures, assume we've reached the end
            if i > 1 and not download_handout(i-1):
                break

if __name__ == "__main__":
    main()
