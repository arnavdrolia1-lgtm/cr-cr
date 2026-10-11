import requests
from PIL import Image
import io

HEADERS = {
    'User-Agent': 'CarSpecApp/2.0 (automotive_app_contact@example.com)'
}

three_models = [
    ("Mercedes-Benz", "EQE", "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/cb/Mercedes-Benz_V295_350%2B_Classic-Days_2022_DSC_0018.jpg/1920px-Mercedes-Benz_V295_350%2B_Classic-Days_2022_DSC_0018.jpg"),
    ("Mercedes-Benz", "EQS", "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/ef/Mercedes-Benz_V297_Classic-Days_2022_DSC_0016.jpg/1920px-Mercedes-Benz_V297_Classic-Days_2022_DSC_0016.jpg"),
    ("Mercedes-Benz", "G Class", "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/38/Mercedes-Benz_W463_G_350_BlueTEC_01.jpg/1920px-Mercedes-Benz_W463_G_350_BlueTEC_01.jpg")
]

for brand, model, url in three_models:
    filename = f"{brand.replace(' ', '_')}_{model.replace(' ', '_')}.jpg"
    dest_path = f"images/{filename}"
    r = requests.get(url, headers=HEADERS, timeout=20)
    print(f"[{brand} {model}] Status: {r.status_code}, Bytes: {len(r.content)}")
    if r.status_code == 200:
        img = Image.open(io.BytesIO(r.content))
        print(f"  Size: {img.size}, Mode: {img.mode}")
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(dest_path, format='JPEG', quality=92)
        print(f"  Successfully saved {dest_path}")
    else:
        print(f"  Failed with status {r.status_code}")
