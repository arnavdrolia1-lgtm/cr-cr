import requests
from PIL import Image
import io
import re

HEADERS = {
    'User-Agent': 'CarSpecApp/2.0 (contact@example.com)'
}

# Search Wikimedia Commons for EQE
search_url = "https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=Mercedes-Benz%20EQE%20front%20white%20studio%20OR%20IAA&format=json"
r = requests.get(search_url, headers=HEADERS, timeout=10).json()
print("Hits:", [h['title'] for h in r.get('query', {}).get('search', [])[:5]])

# Or let's search for Mercedes-Benz V295 images on Wikimedia Commons
cat_url = "https://commons.wikimedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Mercedes-Benz_V295&cmtype=file&cmlimit=15&format=json"
r_cat = requests.get(cat_url, headers=HEADERS, timeout=10).json()
members = r_cat.get('query', {}).get('categorymembers', [])
print("Category files:", [m['title'] for m in members[:10]])

# Get image info for files
for m in members[:5]:
    title = m['title']
    info_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={requests.utils.quote(title)}&prop=imageinfo&iiprop=url|size&format=json"
    r_info = requests.get(info_url, headers=HEADERS, timeout=10).json()
    pages = r_info.get('query', {}).get('pages', {})
    for p in pages.values():
        for ii in p.get('imageinfo', []):
            print(f"{title} -> {ii.get('url')} ({ii.get('width')}x{ii.get('height')})")
