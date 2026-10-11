import os
import datetime

files = [f for f in os.listdir("images") if f.endswith(".jpg")]
file_info = []

for f in files:
    path = os.path.join("images", f)
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    sz = os.path.getsize(path)
    file_info.append((f, mtime, sz))

file_info.sort(key=lambda x: x[1])

print(f"Total files: {len(file_info)}")
print("\nFiles by timestamp:")
for f, mtime, sz in file_info:
    print(f"{mtime.strftime('%Y-%m-%d %H:%M:%S')} | {sz:7d} bytes | {f}")
