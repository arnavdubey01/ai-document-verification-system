import pytesseract
from PIL import Image

import pypdfium2 as pdfium

def extract_text_from_image(file_path):
    image = Image.open(file_path)

    text = pytesseract.image_to_string(image)

    return text

def extract_text_from_pdf(file_path):
    pdf = pdfium.PdfDocument(file_path)

    all_text = []

    for page_number in range (len(pdf)):
        page = pdf[page_number]

        # Render PDF page as an image
        image = page.render(scale = 2).to_pil()

        # Run teseract on the page
        text = pytesseract.image_to_string(image)

        all_text.append(text)

        page.close()

    pdf.close()

    return "\n".join(all_text)

