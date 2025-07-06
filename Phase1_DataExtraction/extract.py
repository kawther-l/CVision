import pytesseract
from pdf2image import convert_from_path
from docx import Document
from PIL import Image
import json
import os

# === CONFIG ===
input_folder = "c:/Users/moi/Desktop/CVision/Phase1_DataExtraction/input_resumes"
output_folder = "c:/Users/moi/Desktop/CVision/Phase1_DataExtraction/extracted_outputs"
os.makedirs(output_folder, exist_ok=True)

# === FUNCTIONS ===
print(f"Looking for files in: {os.path.abspath(input_folder)}")
def ocr_pdf(pdf_path):
    """Extract text from PDF using OCR"""
    text = ""
    try:
        images = convert_from_path(pdf_path, dpi=300)
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")
        return ""
    
    for page_num, img in enumerate(images):
        page_text = pytesseract.image_to_string(img)
        text += f"\n--- Page {page_num + 1} ---\n{page_text}"
    return text

def read_docx(docx_path):
    """Extract text from DOCX"""
    try:
        doc = Document(docx_path)
        full_text = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(full_text)
    except Exception as e:
        print(f"Error reading {docx_path}: {e}")
        return ""

def ocr_image(image_path):
    """Extract text from image files"""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return ""

def save_output(filename, file_type, extracted_text):
    """Save the extracted text to JSON"""
    output_data = {
        "filename": filename,
        "file_type": file_type,
        "char_count": len(extracted_text),
        "raw_text": extracted_text
    }
    output_path = os.path.join(output_folder, f"{filename}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
    print(f"✅ Saved extracted text for {filename} ({len(extracted_text)} chars)")

# === THIS IS THE MAIN LOOP ===
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    extracted_text = ""
    file_type = ""

    if filename.lower().endswith(".pdf"):
        print(f"Processing PDF: {filename}")
        file_type = "PDF"
        extracted_text = ocr_pdf(file_path)

    elif filename.lower().endswith(".docx"):
        print(f"Processing DOCX: {filename}")
        file_type = "DOCX"
        extracted_text = read_docx(file_path)

    elif filename.lower().endswith((".jpg", ".jpeg", ".png")):
        print(f"Processing IMAGE: {filename}")
        file_type = "IMAGE"
        extracted_text = ocr_image(file_path)

    else:
        print(f"⚠ Skipping unsupported file type: {filename}")
        continue

    if extracted_text.strip():
        save_output(filename, file_type, extracted_text)
    else:
        print(f"⚠ No text extracted from {filename}")

print("✅ Phase 1 completed!")
