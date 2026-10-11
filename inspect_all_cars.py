import os
import mysql.connector
from PIL import Image

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Arnav@1909",
    database="AutoSpec_Database_System"
)
cursor = conn.cursor()

cursor.execute("""
    SELECT b.brand_name, m.model_name
    FROM models m
    JOIN brands b ON m.brand_id = b.brand_id
    ORDER BY b.brand_name, m.model_name
""")
db_cars = cursor.fetchall()
conn.close()

print(f"Total car models in DB: {len(db_cars)}")

img_dir = "images"
os.makedirs(img_dir, exist_ok=True)

existing_files = os.listdir(img_dir)
print(f"Total files in images/ folder: {len(existing_files)}")

results = []
for brand, model in db_cars:
    safe_brand = brand.replace(" ", "_")
    safe_model = model.replace(" ", "_")
    filename = f"{safe_brand}_{safe_model}.jpg"
    path = os.path.join(img_dir, filename)
    
    if not os.path.exists(path):
        results.append((brand, model, filename, "MISSING", 0, (0, 0)))
    else:
        sz = os.path.getsize(path)
        try:
            with Image.open(path) as img:
                w, h = img.size
                results.append((brand, model, filename, "EXISTS", sz, (w, h)))
        except Exception as e:
            results.append((brand, model, filename, f"CORRUPT: {e}", sz, (0, 0)))

# Summarize
missing = [r for r in results if r[3] == "MISSING"]
corrupt = [r for r in results if "CORRUPT" in r[3]]
tiny = [r for r in results if r[3] == "EXISTS" and r[4] < 30000] # <30KB

print(f"\nMissing files: {len(missing)}")
for m in missing:
    print(f"  - {m[0]} {m[1]} -> {m[2]}")

print(f"\nCorrupt files: {len(corrupt)}")
for c in corrupt:
    print(f"  - {c[0]} {c[1]} -> {c[2]}")

print(f"\nTiny files (<30KB): {len(tiny)}")
for t in tiny:
    print(f"  - {t[0]} {t[1]} -> {t[2]} ({t[4]} bytes, {t[5]})")
