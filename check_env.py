import sys
import pkg_resources

print("Python version:", sys.version)
installed = {pkg.key for pkg in pkg_resources.working_set}
cv_packages = [p for p in ["torch", "torchvision", "ultralytics", "opencv-python", "cv2", "pillow", "requests", "beautifulsoup4"] if p in installed or p == "cv2"]
print("Relevant installed packages:", cv_packages)
