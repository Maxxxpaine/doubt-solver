import pytesseract
from PIL import Image
import sys

# Set path to tesseract (if it's not already in the system PATH)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path):
    # Open the image using PIL (Pillow)
    image = Image.open(image_path)
    
    # Extract text from the image using Tesseract
    text = pytesseract.image_to_string(image)
    
    return text

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ocr.py <image_path>")
    else:
        image_path = sys.argv[1]  # Get the image path from command-line argument
        text = extract_text_from_image(image_path)
        print("Extracted Text:")
        print(text)
