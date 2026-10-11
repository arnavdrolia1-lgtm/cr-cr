import os
import shutil
from bing_image_downloader import downloader

# Every unique Brand and Model in your database
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

# Ensure the images folder exists
os.makedirs("images", exist_ok=True)

print("Starting automated image download...")

for brand, model in car_models:
    # Format the names exactly as your Streamlit app expects
    safe_brand = brand.replace(" ", "_")
    safe_model = model.replace(" ", "_")
    final_name = f"{safe_brand}_{safe_model}.jpg"
    final_path = os.path.join("images", final_name)

    # Skip if we already downloaded this car
    if os.path.exists(final_path):
        print(f"Skipping {brand} {model}, already exists.")
        continue

    # Craft a specific search query to get a good exterior shot
    search_query = f"{brand} {model} car exterior high quality"
    
    try:
        # Download the top 1 image
        downloader.download(search_query, limit=1, output_dir='temp_img', 
                            adult_filter_off=True, force_replace=False, timeout=15, verbose=False)
        
        # Bing-image-downloader creates a subfolder based on the query. 
        # We need to grab the file out of there and rename it.
        folder_path = os.path.join('temp_img', search_query)
        if os.path.exists(folder_path):
            files = os.listdir(folder_path)
            if files:
                src_file = os.path.join(folder_path, files[0])
                shutil.move(src_file, final_path)
                print(f"✓ Downloaded: {final_name}")
    except Exception as e:
        print(f"X Failed to download {brand} {model}: {e}")

# Clean up the temporary folder
if os.path.exists('temp_img'):
    shutil.rmtree('temp_img')

print("\nFinished! Open your Streamlit app to see the results.")