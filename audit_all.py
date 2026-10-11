import os
from PIL import Image

IMG_DIR = "images"
files = sorted([f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")])

print(f"Total image files: {len(files)}\n")
print(f"{'Filename':<35} | {'Dimensions':<12} | {'Aspect':<6} | {'Size KB':<8}")
print("-" * 70)

suspicious = []
for f in files:
    path = os.path.join(IMG_DIR, f)
    sz = os.path.getsize(path) // 1024
    with Image.open(path) as img:
        w, h = img.size
        aspect = round(w / h, 2)
        print(f"{f:<35} | {f'{w}x{h}':<12} | {aspect:<6} | {sz:<8}")
        # Flag if aspect ratio is odd (e.g. square, portrait, or overly elongated)
        if aspect < 1.15 or aspect > 2.5:
            suspicious.append((f, w, h, aspect, "Weird Aspect Ratio"))
        if sz < 30:
            suspicious.append((f, w, h, aspect, "Very Small File Size"))

print("\n" + "=" * 50)
print(f"Suspicious files based on geometry / size: {len(suspicious)}")
for s in suspicious:
    print(f"  - {s[0]}: {s[1]}x{s[2]} (aspect {s[3]}) - {s[4]}")
