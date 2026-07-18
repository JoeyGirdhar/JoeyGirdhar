import sys
import cv2
import numpy as np
from rembg import remove
from PIL import Image

def prep_image(input_path, output_path="source-prepped.png"):
    print("Isolating face and removing background noise...")
    input_img = Image.open(input_path)
    no_bg = remove(input_img)
    
    img_np = np.array(no_bg)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR)
    alpha = img_np[:, :, 3]
    
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8,8))
    equalized = clahe.apply(gray)
    
    output = np.where(alpha == 0, 255, equalized)
    
    cv2.imwrite(output_path, output)
    print(f"Success! Prepped source asset saved as: {output_path}")

if __name__ == "__main__":
    prep_image("source-photo.jpg")
