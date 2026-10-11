import os
import sys
import shutil
import tempfile
from PIL import Image
from bing_image_downloader import downloader

# Ensure standard UTF-8 console output across Windows shells
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

car_models = [
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
    ("Jaguar", "F-Pace")
]

def main():
    target_dir = os.path.join(os.getcwd(), "images")
    os.makedirs(target_dir, exist_ok=True)

    print("==================================================")
    print("AutoSpec Vehicle Exterior Image Downloader")
    print(f"Target Directory: {target_dir}")
    print(f"Total Vehicles to Process: {len(car_models)}")
    print("==================================================\n")

    temp_dir = tempfile.mkdtemp(prefix="bing_car_dl_")

    downloaded_count = 0
    skipped_count = 0
    failed_count = 0

    try:
        for idx, (brand, model) in enumerate(car_models, start=1):
            # Target filename format: Brand_Model.jpg (spaces replaced with _)
            safe_brand = brand.replace(" ", "_")
            safe_model = model.replace(" ", "_")
            target_filename = f"{safe_brand}_{safe_model}.jpg"
            target_file_path = os.path.join(target_dir, target_filename)

            # Check if file already exists
            if os.path.exists(target_file_path) and os.path.getsize(target_file_path) > 0:
                print(f"[{idx:02d}/{len(car_models):02d}] [SKIP] '{target_filename}' (Already exists)")
                skipped_count += 1
                continue

            print(f"[{idx:02d}/{len(car_models):02d}] [DOWNLOADING] {brand} {model} -> '{target_filename}'...")

            # Candidate search queries starting with required format
            queries = [
                f"{brand} {model} car exterior high quality",
                f"{brand} {model} car exterior",
                f"{brand} {model} official car"
            ]

            saved = False
            for q_idx, query in enumerate(queries, start=1):
                try:
                    query_temp_dir = os.path.join(temp_dir, f"car_{idx}_{q_idx}")
                    os.makedirs(query_temp_dir, exist_ok=True)

                    downloader.download(
                        query,
                        limit=1,
                        output_dir=query_temp_dir,
                        adult_filter_off=True,
                        force_replace=True,
                        timeout=15,
                        verbose=False
                    )

                    # Locate the downloaded image file
                    downloaded_file = None
                    for root, _, files in os.walk(query_temp_dir):
                        for file in files:
                            full_path = os.path.join(root, file)
                            if os.path.isfile(full_path) and os.path.getsize(full_path) > 0:
                                downloaded_file = full_path
                                break
                        if downloaded_file:
                            break

                    if downloaded_file:
                        try:
                            with Image.open(downloaded_file) as img:
                                rgb_img = img.convert("RGB")
                                rgb_img.save(target_file_path, "JPEG", quality=92)
                            size_kb = os.path.getsize(target_file_path) // 1024
                            print(f"       [SAVED] '{target_filename}' ({size_kb} KB, query '{query}')")
                            downloaded_count += 1
                            saved = True
                        except Exception:
                            shutil.copy2(downloaded_file, target_file_path)
                            print(f"       [COPIED] '{target_filename}' (fallback copy, query '{query}')")
                            downloaded_count += 1
                            saved = True

                    shutil.rmtree(query_temp_dir, ignore_errors=True)

                    if saved:
                        break

                except Exception as e:
                    pass

            if not saved:
                print(f"       [WARN] Could not retrieve image for {brand} {model} across queries.")
                failed_count += 1

    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
            print("\n[CLEANUP] Temporary download cache removed cleanly.")

    print("\n==================================================")
    print("Download Summary:")
    print(f"  Total Processed: {len(car_models)}")
    print(f"  Newly Downloaded: {downloaded_count}")
    print(f"  Skipped (Existing): {skipped_count}")
    print(f"  Failed: {failed_count}")
    total_imgs = len([f for f in os.listdir(target_dir) if f.lower().endswith('.jpg')])
    print(f"  Total in 'images/' folder: {total_imgs} / {len(car_models)}")
    print("==================================================")

if __name__ == "__main__":
    main()
