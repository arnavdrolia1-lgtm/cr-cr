import os
import sys
import io
import time
import re
import html
import hashlib
import urllib.request
import urllib.parse
from PIL import Image

# Ensure standard UTF-8 console output across Windows shells
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

# The complete list of 56 original luxury models + 48 Indian market models (104 total)
CAR_MODELS = [
    # --- Original 56 models ---
    ("BMW", "X1"), ("BMW", "X3"), ("BMW", "X5"), ("BMW", "X7"), ("BMW", "XM"), 
    ("BMW", "iX1 LWB"), ("BMW", "iX"), ("BMW", "2 Series"), ("BMW", "3 Series LWB"), 
    ("BMW", "3 Series"), ("BMW", "5 Series"), ("BMW", "7 Series"), ("BMW", "i4"), 
    ("BMW", "i5"), ("BMW", "i7"), ("BMW", "M2"), ("BMW", "M4"), ("BMW", "M5"), 
    ("BMW", "M8"), ("BMW", "Z4"),
    ("Audi", "A4"), ("Audi", "A6"), ("Audi", "S5"), ("Audi", "Q3"), ("Audi", "Q5"), 
    ("Audi", "Q7"), ("Audi", "Q8"), ("Audi", "Q8 e-tron"), ("Audi", "Q8 Sportback e-tron"), 
    ("Audi", "RS e-tron GT"),
    ("Mercedes-Benz", "A Class"), ("Mercedes-Benz", "C Class"), ("Mercedes-Benz", "C Class AMG"), 
    ("Mercedes-Benz", "E Class"), ("Mercedes-Benz", "S Class"), ("Mercedes-Benz", "S Class AMG"), 
    ("Mercedes-Benz", "EQA"), ("Mercedes-Benz", "EQB"), ("Mercedes-Benz", "EQE"), 
    ("Mercedes-Benz", "EQS"), ("Mercedes-Benz", "GLA"), ("Mercedes-Benz", "GLA AMG"), 
    ("Mercedes-Benz", "GLC"), ("Mercedes-Benz", "GLE"), ("Mercedes-Benz", "GLE AMG"), 
    ("Mercedes-Benz", "GLS"), ("Mercedes-Benz", "GLS AMG"), ("Mercedes-Benz", "G Class"), 
    ("Mercedes-Benz", "G Class AMG"), ("Mercedes-Benz", "CLE Cabriolet AMG"),
    ("Volvo", "EX30"), ("Volvo", "EX40"), ("Volvo", "EC40"), ("Volvo", "XC60"), ("Volvo", "XC90"),
    ("Jaguar", "F-Pace"),

    # --- Indian Market & Supercar additions ---
    ("Ford", "Endeavour"), ("Ford", "Mustang"),
    ("Mahindra", "XUV700"), ("Mahindra", "Scorpio-N"), ("Mahindra", "Thar"),
    ("Hyundai", "Creta"), ("Hyundai", "Venue"), ("Hyundai", "Verna"), ("Hyundai", "Bayon"),
    ("Honda", "City"), ("Honda", "Elevate"),
    ("Maruti Suzuki", "Swift"), ("Maruti Suzuki", "Brezza"), ("Maruti Suzuki", "Grand Vitara"),
    ("Tata Motors", "Nexon"), ("Tata Motors", "Harrier"), ("Tata Motors", "Safari"),
    ("Tata Motors", "Punch"), ("Tata Motors", "Sierra"), ("Tata Motors", "Curvv"), ("Tata Motors", "Aeris"),
    ("Kia", "Seltos"), ("Kia", "Sonet"), ("Kia", "EV6"),
    ("Toyota", "Fortuner"), ("Toyota", "Innova Hycross"), ("Toyota", "Urban Cruiser Hyryder"),
    ("MG Motor", "Hector"), ("MG Motor", "ZS EV"),
    ("Volkswagen", "Virtus"), ("Volkswagen", "Taigun"),
    ("Skoda", "Slavia"), ("Skoda", "Kushaq"),
    ("Jeep", "Compass"), ("Jeep", "Wrangler"),
    ("BYD", "Atto 3"), ("BYD", "Seal"),
    ("Land Rover", "Range Rover"), ("Land Rover", "Defender"),
    ("Porsche", "911"), ("Porsche", "Macan"), ("Porsche", "Taycan"),
    ("Lexus", "RX"), ("Lexus", "ES"),
    ("Ferrari", "Roma"), ("Ferrari", "296 GTB"),
    ("Lamborghini", "Urus"), ("Lamborghini", "Revuelto")
]

def get_image_candidates(query, count=10):
    """Fetches image URL candidates using Bing Image search with strict photo/aspect filters."""
    params = urllib.parse.urlencode({
        'q': query,
        'count': count,
        'adlt': 'on', # Strict safe search to prevent irrelevant/adult thumbnails
        'qft': '+filterui:photo-photo+filterui:aspect-wide'
    })
    url = f"https://www.bing.com/images/async?{params}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            links = re.findall(r'murl&quot;:&quot;(.*?)&quot;', content)
            return [html.unescape(l).replace(' ', '%20') for l in links]
    except Exception:
        return []

def get_wikipedia_fallback_image(brand, model):
    """Wikipedia search fallback for accurate automotive lead images."""
    try:
        query = f"{brand} {model}"
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&utf8=&format=json&srlimit=1"
        req = urllib.request.Request(search_url, headers={'User-Agent': 'AutoSpecApp/2.0 (contact@autospec.test)'})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode())
            results = data.get('query', {}).get('search', [])
            if not results:
                return None
            title = results[0]['title']

        img_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=pageimages&format=json&pithumbsize=1600"
        req2 = urllib.request.Request(img_url, headers={'User-Agent': 'AutoSpecApp/2.0 (contact@autospec.test)'})
        with urllib.request.urlopen(req2, timeout=6) as resp2:
            data2 = json.loads(resp2.read().decode())
            pages = data2.get('query', {}).get('pages', {})
            for _, pdata in pages.items():
                if 'thumbnail' in pdata:
                    return pdata['thumbnail']['source']
    except Exception:
        pass
    return None

def download_and_verify(links, seen_hashes, min_w=600, min_h=350):
    """
    Downloads image candidates and strictly verifies:
    1. Valid image format (JPEG, PNG, WEBP)
    2. File size between 25 KB and 8 MB
    3. Minimum dimensions (width >= 600, height >= 350)
    4. Aspect ratio is landscape (1.1 <= ratio <= 2.5)
    5. MD5 hash is globally unique (rejects duplicate images)
    """
    for link in links:
        try:
            req = urllib.request.Request(link, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()

            if len(data) < 25000 or len(data) > 8000000:
                continue

            h = hashlib.md5(data).hexdigest()
            if h in seen_hashes:
                continue

            img = Image.open(io.BytesIO(data))
            if img.format not in ('JPEG', 'PNG', 'WEBP'):
                continue

            w, h_dim = img.size
            if w < min_w or h_dim < min_h:
                continue

            ratio = w / h_dim
            if not (1.1 <= ratio <= 2.5):
                continue

            # Convert to clean RGB JPEG
            rgb_img = img.convert('RGB')
            seen_hashes.add(h)
            return rgb_img, h, link
        except Exception:
            continue

    return None, None, None

def main():
    target_dir = os.path.join(os.getcwd(), "images")
    os.makedirs(target_dir, exist_ok=True)

    print("==================================================")
    print("AutoSpec High-Precision Exterior Image Downloader")
    print(f"Target Directory: {target_dir}")
    print(f"Total Vehicles: {len(CAR_MODELS)}")
    print("==================================================\n")

    # Purge existing corrupted duplicate/junk files
    # Any file that is part of known duplicates or under 20KB or square/corrupted
    known_duplicate_hashes = {
        '2697678282271a0244ea453df2d93d7b', # Duplicate 5-series on all 20 BMWs
        'f923b7e42d76a7e0f2187f59d4793610', # Chalukyas map
        '8fa5a44359be2616f081498fa66395dc', # Police crowd thumbnail
        '7db410c52bb53c15aa31fe18260a924b', # Romantic movie GIF
    }

    seen_hashes = set()
    cleaned_count = 0

    print("Inspecting existing images...")
    for f in os.listdir(target_dir):
        if not f.lower().endswith('.jpg'):
            continue
        p = os.path.join(target_dir, f)
        try:
            sz = os.path.getsize(p)
            data = open(p, 'rb').read()
            h = hashlib.md5(data).hexdigest()
            
            # Check if file is corrupt, duplicate, or junk
            im = Image.open(p)
            w, h_dim = im.size
            ratio = w / h_dim

            if (h in known_duplicate_hashes or 
                h in seen_hashes or 
                sz < 25000 or 
                w < 500 or h_dim < 300 or 
                ratio < 1.05 or ratio > 2.6):
                os.remove(p)
                cleaned_count += 1
                print(f"  [REMOVED JUNK/DUPLICATE] {f} ({w}x{h_dim}, {sz//1024} KB)")
            else:
                seen_hashes.add(h)
        except Exception:
            try:
                os.remove(p)
                cleaned_count += 1
            except Exception:
                pass

    print(f"Purged {cleaned_count} invalid/duplicate images from {target_dir}.\n")

    downloaded = 0
    skipped = 0
    failed = 0

    for idx, (brand, model) in enumerate(CAR_MODELS, start=1):
        safe_brand = brand.replace(" ", "_")
        safe_model = model.replace(" ", "_")
        filename = f"{safe_brand}_{safe_model}.jpg"
        filepath = os.path.join(target_dir, filename)

        # Check if high-quality file already exists
        if os.path.exists(filepath) and os.path.getsize(filepath) >= 25000:
            try:
                im = Image.open(filepath)
                if im.size[0] >= 600 and im.size[1] >= 350:
                    print(f"[{idx:03d}/{len(CAR_MODELS):03d}] [EXISTS] {filename} ({im.size[0]}x{im.size[1]})")
                    skipped += 1
                    continue
            except Exception:
                pass

        print(f"[{idx:03d}/{len(CAR_MODELS):03d}] [FETCHING] {brand} {model}...")

        # Formulate targeted queries
        queries = [
            f"{brand} {model} car exterior",
            f"{brand} {model} front quarter view car",
            f"{brand} {model} official car photo",
            f"{brand} {model} car"
        ]

        saved = False
        for q in queries:
            links = get_image_candidates(q, count=8)
            img, img_hash, link = download_and_verify(links, seen_hashes)
            if img:
                img.save(filepath, "JPEG", quality=92)
                sz_kb = os.path.getsize(filepath) // 1024
                print(f"        [SAVED] {filename} ({img.size[0]}x{img.size[1]}, {sz_kb} KB)")
                downloaded += 1
                saved = True
                break
            time.sleep(0.4)

        if not saved:
            # Fallback query with relaxed constraints
            links = get_image_candidates(f"{brand} {model} exterior", count=12)
            img, img_hash, link = download_and_verify(links, seen_hashes, min_w=500, min_h=300)
            if img:
                img.save(filepath, "JPEG", quality=92)
                sz_kb = os.path.getsize(filepath) // 1024
                print(f"        [SAVED (Fallback)] {filename} ({img.size[0]}x{img.size[1]}, {sz_kb} KB)")
                downloaded += 1
                saved = True

        if not saved:
            print(f"        [WARN] Failed to find valid image for {brand} {model}")
            failed += 1

        time.sleep(0.3)

    print("\n==================================================")
    print("Download Summary:")
    print(f"  Total Processed : {len(CAR_MODELS)}")
    print(f"  Newly Saved     : {downloaded}")
    print(f"  Already Valid   : {skipped}")
    print(f"  Failed          : {failed}")
    total_in_dir = len([f for f in os.listdir(target_dir) if f.lower().endswith('.jpg')])
    print(f"  Total in images/: {total_in_dir} / {len(CAR_MODELS)}")
    print("==================================================")

if __name__ == "__main__":
    main()
