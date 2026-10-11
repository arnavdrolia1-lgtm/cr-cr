import os
import re
import requests
from PIL import Image
import io
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'CarSpecApp/2.0 (automotive_app_contact@example.com)'
}

# The 26 tainted models with specific Wikipedia page searches/titles
TARGETS = [
    ("Audi", "A4", "Audi A4"),
    ("Audi", "S5", "Audi S5"),
    ("Audi", "Q5", "Audi Q5"),
    ("Audi", "Q8 Sportback e-tron", "Audi Q8 e-tron"),
    ("Audi", "RS e-tron GT", "Audi e-tron GT"),
    ("Mercedes-Benz", "A Class", "Mercedes-Benz A-Class"),
    ("Mercedes-Benz", "C Class", "Mercedes-Benz C-Class"),
    ("Mercedes-Benz", "C Class AMG", "Mercedes-AMG C-Class"),
    ("Mercedes-Benz", "S Class", "Mercedes-Benz S-Class"),
    ("Mercedes-Benz", "S Class AMG", "Mercedes-AMG GT 4-Door Coupe"),
    ("Mercedes-Benz", "EQB", "Mercedes-Benz EQB"),
    ("Mercedes-Benz", "EQE", "Mercedes-Benz EQE"),
    ("Mercedes-Benz", "EQS", "Mercedes-Benz EQS"),
    ("Mercedes-Benz", "GLA", "Mercedes-Benz GLA"),
    ("Mercedes-Benz", "GLC", "Mercedes-Benz GLC"),
    ("Mercedes-Benz", "GLE", "Mercedes-Benz GLE"),
    ("Mercedes-Benz", "GLS AMG", "Mercedes-Benz GLS"),
    ("Mercedes-Benz", "G Class", "Mercedes-Benz G-Class"),
    ("Mercedes-Benz", "G Class AMG", "Mercedes-AMG G 63"),
    ("Mercedes-Benz", "CLE Cabriolet AMG", "Mercedes-Benz CLE"),
    ("Volvo", "EX30", "Volvo EX30"),
    ("Volvo", "EX40", "Volvo XC40 Recharge"),
    ("Volvo", "EC40", "Volvo C40 Recharge"),
    ("Volvo", "XC60", "Volvo XC60"),
    ("Volvo", "XC90", "Volvo XC90"),
    ("Jaguar", "F-Pace", "Jaguar F-Pace")
]

IMG_DIR = "images"
os.makedirs(IMG_DIR, exist_ok=True)

def fetch_wiki_car_image(query):
    # Search Wikipedia
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(query + ' car')}&format=json"
    res = requests.get(search_url, headers=HEADERS, timeout=10).json()
    hits = res.get('query', {}).get('search', [])
    for hit in hits[:5]:
        title = hit['title']
        if any(term in title.lower() for term in ['list of', 'timeline', 'concept', 'formula', 'crash']):
            continue
        sum_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(title)}"
        s = requests.get(sum_url, headers=HEADERS, timeout=10).json()
        orig = s.get('originalimage', {}).get('source')
        thumb = s.get('thumbnail', {}).get('source')
        img_url = orig or thumb
        if img_url:
            # Check if svg or logo
            if img_url.endswith('.svg') or img_url.endswith('.svg.png') or 'logo' in img_url.lower():
                continue
            # Try to get high resolution version (1280px)
            if thumb and not orig:
                img_url = re.sub(r'/\d+px-', '/1280px-', thumb)
            return img_url, title
    return None, None

def download_and_validate(url):
    resp = requests.get(url, headers=HEADERS, timeout=20)
    if resp.status_code == 200:
        img_bytes = resp.content
        img = Image.open(io.BytesIO(img_bytes))
        w, h = img.size
        # Must be landscape car photo and reasonable size
        if w >= 500 and h >= 300 and (w / h) >= 1.1:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=92)
            return buf.getvalue(), w, h
    return None, 0, 0

print("Starting replacement of 26 tainted legacy files...\n", flush=True)

success_count = 0
for brand, model, query in TARGETS:
    filename = f"{brand.replace(' ', '_')}_{model.replace(' ', '_')}.jpg"
    dest_path = os.path.join(IMG_DIR, filename)
    
    print(f"[{brand} {model}] Processing...", flush=True)
    img_url, title = fetch_wiki_car_image(query)
    if not img_url:
        print(f"  [FAIL] No Wikipedia image found for {query}", flush=True)
        continue
    
    print(f"  Found from '{title}': {img_url[:70]}...", flush=True)
    jpeg_bytes, w, h = download_and_validate(img_url)
    if jpeg_bytes:
        # Delete old file
        if os.path.exists(dest_path):
            os.remove(dest_path)
        with open(dest_path, "wb") as f:
            f.write(jpeg_bytes)
        print(f"  [OK] Saved {filename} ({w}x{h}, {len(jpeg_bytes)} bytes)", flush=True)
        success_count += 1
    else:
        print(f"  [FAIL] Validation failed for {img_url}", flush=True)

print(f"\nDone! Successfully updated {success_count}/{len(TARGETS)} files.", flush=True)
