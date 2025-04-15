import easyocr
import cv2
import os
import numpy as np
# import matplotlib.pyplot as plt

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])


def is_text_properly_aligned(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Preprocessing - Binarization
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Extract text with bounding boxes
    results = reader.readtext(thresh)

    if not results:
        return True  # No text detected, consider it aligned

    # Extract y-coordinates of detected text
    y_positions = [box[0][1] for box, text, conf in results]

    # Sort y-coordinates and check alignment
    y_positions.sort()
    base_y = y_positions[0]  # First detected text baseline

    for y in y_positions:
        if abs(y - base_y) > 10:  # Tolerance for misalignment
            return False  # Misaligned text detected
    
    return True  # Text is properly aligned


# Folder containing images
image_folder = r"C:\Users\jjers\OneDrive\Pictures\Sample"
error_images = []

# Iterate through images
for filename in os.listdir(image_folder):
    if filename.endswith((".jpg", ".png", ".jpeg")):
        image_path = os.path.join(image_folder, filename)
        if not is_text_properly_aligned(image_path):
            error_images.append(filename)

# Output filenames of misaligned images
for img in error_images:
    print(img)