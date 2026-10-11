import os
import re
import requests
from PIL import Image
import io

HEADERS = {
    'User-Agent': 'CarSpecApp/2.0 (automotive_app_contact@example.com)'
}

models_to_fix = [
    ("Audi", "A4", "Audi A4 car"),
    ("Audi", "S5", "Audi S5 car"),
    ("Audi", "Q5", "Audi Q5 car"),
    ("Audi", "Q8 Sportback e-tron", "Audi Q8 e-tron Sportback car"),
    ("Audi", "RS e-tron GT", "Audi e-tron GT car"),
    ("Mercedes-Benz", "A Class", "Mercedes-Benz A-Class car"),
    ("Mercedes-Benz", "C Class", "Mercedes-Benz C-Class car"),
    ("Mercedes-Benz", "C Class AMG", "Mercedes-AMG C 63 car"),
    ("Mercedes-Benz", "S Class", "Mercedes-Benz S-Class car"),
    ("Mercedes-Benz", "S Class AMG", "Mercedes-AMG S 63 car"),
    ("Mercedes-Benz", "EQB", "Mercedes-Benz EQB car"),
    ("Mercedes-Benz", "EQE", "Mercedes-Benz EQE car"),
    ("Mercedes-Benz", "EQS", "Mercedes-Benz EQS car"),
    ("Mercedes-Benz", "GLA", "Mercedes-Benz GLA car"),
    ("Mercedes-Benz", "GLC", "Mercedes-Benz GLC car"),
    ("Mercedes-Benz", "GLE", "Mercedes-Benz GLE car"),
    ("Mercedes-Benz", "GLS AMG", "Mercedes-AMG GLS 63 car"),
    ("Mercedes-Benz", "G Class", "Mercedes-Benz G-Class car"),
    ("Mercedes-Benz", "G Class AMG", "Mercedes-AMG G 63 car"),
    ("Mercedes-Benz", "CLE Cabriolet AMG", "Mercedes-Benz CLE car"),
    ("Volvo", "EX30", "Volvo EX30 car"),
    ("Volvo", "EX40", "Volvo EX40 car"),
    ("Volvo", "EC40", "Volvo EC40 car"),
    ("Volvo", "XC60", "Volvo XC60 car"),
    ("Volvo", "XC90", "Volvo XC90 car"),
    ("Jaguar", "F-Pace", "Jaguar F-Pace car")
]

def get_wiki_image_url(query):
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(query)}&format=json"
    r = requests.get(search_url, headers=HEADERS, timeout=10).json()
    hits = r.get('query', {}).get('search', [])
    for hit in hits[:3]:
        title = hit['title']
        sum_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(title)}"
        s = requests.get(sum_url, headers=HEADERS, timeout=10).json()
        orig = s.get('originalimage', {}).get('source')
        thumb = s.get('thumbnail', {}).get('source')
        # We can upscale thumbnail from 330px to 1280px by replacing /330px- with /1280px-
        if orig:
            return orig, title
        if thumb:
            high_res = re.sub(r'/\d+px-', '/1280px-', thumb)
            return high_res, title
    return None, None

for brand, model, query in models_to_fix:
    url, title = get_wiki_image_url(query)
    print(f"[{brand} {model}] -> ({title}) -> {url}")
