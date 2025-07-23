# batch_extractor_2_2.py
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
import re
import os

# MODIFY THIS PATH IF NECESSARY
# For Windows
# pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# For Linux/Mac, comment out or use your local path
# pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def preprocess_image(img):
    img = img.convert('L')  # Grayscale
    img = img.resize((img.width * 2, img.height * 2))  # Upscale
    img = img.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.5)
    return img

def extract_using_ocr(path):
    text = ""
    try:
        images = []
        if path.lower().endswith(('.png', '.jpg', '.jpeg')):
            images = [Image.open(path)]
        else:
            images = convert_from_path(path, dpi=300)

        for img in images:
            img = preprocess_image(img)
            text += pytesseract.image_to_string(img, lang='eng', config='--psm 6') + "\n"

    except Exception as e:
        print("OCR Error:", e)
    return text

def extract_from_file(file_path):
    text = ""

    # Attempt PDF text extraction first
    if file_path.lower().endswith(".pdf"):
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except:
            text = ""

    # Fallback to OCR if text is missing or doesn't contain key fields
    if not text.strip() or "Roll" not in text:
        text = extract_using_ocr(file_path)

    cleaned_text = text.replace("\r", " ").replace("\n", "\n")

    # Extract roll number
    roll = "N/A"
    roll_match = re.search(r"(Roll\s*No\.?|Roll\s*Number|Roll[Ii]No|RollINo)\s*[:\-]?\s*(\d{9,})", cleaned_text, re.IGNORECASE)
    if roll_match:
        roll = roll_match.group(2).strip()
    
    if(roll== "N/A"):
        roll_candidates = re.findall(r"\d{10,15}", cleaned_text)
        for candidate in roll_candidates:
            if candidate.startswith("220") and len(candidate) == 13:
                roll = candidate
                break
    

    # Extract name
    # name = "N/A"
    # name_candidates = re.findall(r"(?:Name)\s*[:\-]?\s*([A-Z][A-Z\s]{3,50})", cleaned_text)
    # for candidate in name_candidates:
    #     cleaned = candidate.strip()
    #     if all(x not in cleaned.lower() for x in ["father", "course", "code", "branch", "hindi", "engineering"]):
    #         words = cleaned.split()
    #         if 1 <= len(words) <= 4:
    #             # Remove any trailing ' H', ' F', or ' HF' at the end of the name
    #             name = re.sub(r'\s+(H|F|HF)$', '', cleaned)
    #             break
    # name = "N/A"

    # # Go line-by-line and only look at lines with the word 'Name'
    # for line in cleaned_text.splitlines():
    #     if "Name" in line:
    #         # Try to extract name after label
    #         match = re.search(r"(?:Name|Student Name)\s*[:\-]?\s*([A-Z][A-Z\s]{2,50})", line)
    #         if match:
    #             candidate = match.group(1).strip()
    #             # Skip junk like "Father", etc.
    #             if all(x not in candidate.lower() for x in ["father", "course", "code", "branch", "hindi", "engineering"]):
    #                 # Only accept up to 4 words (likely a real name)
    #                 words = candidate.split()
    #                 if 1 <= len(words) <= 4:
    #                     # Remove trailing junk like 'H', 'F', 'HF'
    #                     name = re.sub(r'\s+(H|F|HF)$', '', candidate)
    #                     break

# Extract name
    name = "N/A"
    for line in cleaned_text.splitlines():
        # Only consider lines that begin with "Name"
        if re.match(r"^\s*Name\s*[:\-]", line):
            match = re.search(r"Name\s*[:\-]?\s*([A-Z][A-Z\s]{2,50})", line)
            if match:
                candidate = match.group(1).strip()
                if all(x not in candidate.lower() for x in ["father", "course", "code", "branch", "hindi", "engineering"]):
                    words = candidate.split()
                    if 1 <= len(words) <= 4:
                        name = re.sub(r'\s+(H|F|HF)$', '', candidate)
                        break


    # Extract SGPA
    sgpa_matches = re.findall(r"SGPA\s*[:\-]?\s*([\d\.]{1,4})", cleaned_text)
    sgpas = [float(s) for s in sgpa_matches if re.match(r'^\d+(\.\d+)?$', s)]

    return {
        "filename": os.path.basename(file_path),
        "name": name,
        "roll": roll,
        "sgpas": sgpas,
        "raw_text": cleaned_text  # for optional display
    }
