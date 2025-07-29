import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

def check_plagiarism(text):
    query = '+'.join(text.split()[:8])
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except Exception as e:
        return {'error': 'Google search failed', 'details': str(e)}

    if response.status_code != 200:
        return {'error': 'Google search failed', 'status_code': response.status_code}

    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a') if 'http' in str(a.get('href'))]

    matches = 0
    total = 0

    for link in links[:5]:  # limit to 5 pages
        try:
            page = requests.get(link, headers=headers, timeout=5)
            page_text = BeautifulSoup(page.text, 'html.parser').get_text()
            similarity = SequenceMatcher(None, text, page_text).ratio()
            if similarity > 0.75:
                matches += 1
            total += 1
        except:
            continue

    plag_percent = (matches / total) * 100 if total > 0 else 0
    return {'plag_percent': round(plag_percent, 2)}
