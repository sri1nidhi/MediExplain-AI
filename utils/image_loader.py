from PIL import Image
import pytesseract

def extract_image_text(image_file):
    

    image = Image.open(image_file)

    text = pytesseract.image_to_string(image)

    return text