import requests
from bs4 import BeautifulSoup
import hashlib

def check_plagiarism(text):
    query = '+'.join(text.split()[:8])  # Use first 8 words for Google search
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except Exception as e:
        return {'error': 'Google search failed', 'details': str(e)}

    if response.status_code != 200:
        return {'error': 'Google search failed', 'status_code': response.status_code}

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    
    hashes = []
    original_hash = hashlib.md5(text.encode('utf-8')).hexdigest()

    for link in links[:5]:
        href = link.get('href')
        if href and 'http' in href:
            try:
                page = requests.get(href, headers=headers, timeout=5)
                page_text = BeautifulSoup(page.text, 'html.parser').get_text()
                page_hash = hashlib.md5(page_text.encode('utf-8')).hexdigest()
                hashes.append(page_hash)
            except:
                continue

    match_count = hashes.count(original_hash)
    plag_percent = (match_count / len(hashes)) * 100 if hashes else 0.0
    return {'plag_percent': round(plag_percent, 2)}
