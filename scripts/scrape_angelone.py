import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.angelone.in/support"
VISITED = set()


def scrape(url, depth=0):
    if url in VISITED or depth > 2:
        return ""
    print(f"Scraping: {url}")
    VISITED.add(url)
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        content = soup.get_text(separator=" ", strip=True)
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith(BASE_URL)]
        texts = [content]
        for link in links:
            time.sleep(1)
            texts.append(scrape(link, depth + 1))
        return "\n".join(texts)
    except:
        return ""

if __name__ == "__main__":
    full_text = scrape(BASE_URL)
    with open("../data/angelone_support.txt", "w") as f:
        f.write(full_text)
    print("Finished scraping AngelOne support site.")