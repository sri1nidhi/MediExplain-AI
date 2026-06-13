from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def extract_image_text(uploaded_file):

    image = Image.open(uploaded_file)

    text = pytesseract.image_to_string(image)

    return text