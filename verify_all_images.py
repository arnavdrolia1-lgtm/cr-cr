import os
import cv2
import sys

sys.stdout.reconfigure(encoding='utf-8')

IMG_DIR = "images"
cascade_dir = cv2.data.haarcascades
face_cascade = cv2.CascadeClassifier(os.path.join(cascade_dir, 'haarcascade_frontalface_default.xml'))
profile_cascade = cv2.CascadeClassifier(os.path.join(cascade_dir, 'haarcascade_profileface.xml'))
upper_cascade = cv2.CascadeClassifier(os.path.join(cascade_dir, 'haarcascade_upperbody.xml'))
full_cascade = cv2.CascadeClassifier(os.path.join(cascade_dir, 'haarcascade_fullbody.xml'))

files = sorted([f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")])
print(f"Total images to inspect: {len(files)}\n")

flagged = []

for f in files:
    path = os.path.join(IMG_DIR, f)
    img = cv2.imread(path)
    if img is None:
        print(f"[ERROR] Cannot read image: {f}")
        flagged.append((f, "UNREADABLE"))
        continue
    
    h, w, c = img.shape
    aspect = w / h
    
    # Check orientation
    if aspect < 1.0:
        print(f"[FLAGGED ORIENTATION] {f}: Portrait orientation ({w}x{h})")
        flagged.append((f, "PORTRAIT"))
        continue

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Resize for faster and more reliable Haar detection if huge
    scale = 1.0
    if w > 1200:
        scale = 1200.0 / w
        gray_small = cv2.resize(gray, (1200, int(h * scale)))
    else:
        gray_small = gray

    # Detect faces
    faces = face_cascade.detectMultiScale(gray_small, scaleFactor=1.15, minNeighbors=5, minSize=(30, 30))
    profiles = profile_cascade.detectMultiScale(gray_small, scaleFactor=1.15, minNeighbors=5, minSize=(30, 30))
    bodies = full_cascade.detectMultiScale(gray_small, scaleFactor=1.15, minNeighbors=4, minSize=(50, 100))
    uppers = upper_cascade.detectMultiScale(gray_small, scaleFactor=1.15, minNeighbors=4, minSize=(40, 40))

    detections = []
    if len(faces) > 0:
        detections.append(f"{len(faces)} face(s)")
    if len(profiles) > 0:
        detections.append(f"{len(profiles)} profile face(s)")
    if len(bodies) > 0:
        detections.append(f"{len(bodies)} full body/person(s)")
    if len(uppers) > 0:
        detections.append(f"{len(uppers)} upper body(s)")

    if detections:
        print(f"[FLAGGED PERSON/FACE] {f} ({w}x{h}): {', '.join(detections)}")
        flagged.append((f, ", ".join(detections)))

print("\n" + "="*50)
print(f"Scan complete. Total flagged images: {len(flagged)}")
for item in flagged:
    print(f"  - {item[0]}: {item[1]}")
print("="*50)
