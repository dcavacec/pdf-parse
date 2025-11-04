from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf_images(pdf_path):
    """
    Extracts text from a PDF by converting it to images and using OCR.
    """
    # Convert PDF to a list of PIL Image objects
    images = convert_from_path(pdf_path)

    all_text = ""
    for i, img in enumerate(images):
        print(f"Processing page {i+1}...")
        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(img)
        all_text += f"--- Page {i+1} ---\n"
        all_text += text + "\n"
    
    return all_text

# Replace 'your_document.pdf' with the path to your PDF file
pdf_file_path = 'data/ces-19-1_5.pdf'
extracted_text = extract_text_from_pdf_images(pdf_file_path)

# Print the extracted text or save it to a file
print(extracted_text)