import requests

headers = {'User-Agent': 'CarSpecApp/1.0 (test@example.com)'}

test_models = [
    "Audi A4", "Audi S5", "Audi Q5", "Audi RS e-tron GT",
    "Mercedes-Benz A-Class", "Mercedes-Benz C-Class", "Mercedes-Benz S-Class",
    "Mercedes-Benz GLC", "Mercedes-Benz GLE", "Mercedes-Benz G-Class",
    "Volvo EX30", "Volvo XC60", "Volvo XC90", "Jaguar F-Pace"
]

for model in test_models:
    # 1. Search Wikipedia
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(model + ' car')}&format=json"
    r = requests.get(search_url, headers=headers).json()
    hits = r.get('query', {}).get('search', [])
    if hits:
        title = hits[0]['title']
        # Get page summary
        sum_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(title)}"
        s = requests.get(sum_url, headers=headers).json()
        orig = s.get('originalimage', {}).get('source')
        thumb = s.get('thumbnail', {}).get('source')
        print(f"[{model}] -> {title} -> {thumb or orig}")
    else:
        print(f"[{model}] -> No search hits")
