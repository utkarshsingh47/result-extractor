# 📄 Result Extractor

A Python-based tool to extract **Name**, **Roll Number**, and **SGPA** values from AKTU result PDFs or scanned images.  
Supports **multiple file uploads**, **OCR fallback**, and **Streamlit web interface**.

---

## 🚀 Features

- ✅ Extracts key fields like Name, Roll No., SGPA
- 📄 Works with PDF or image uploads
- 🔍 Option to view raw OCR/text output for debugging
- 🔍 **OCR fallback** for scanned or non-searchable PDFs.
- 📥 Download extracted results as a CSV

---

## 🧠 How It Works

1. Attempts to extract readable text using `pdfplumber`
2. If the PDF is scanned or unreadable, falls back to **OCR using Tesseract** (if enabled)
3. Extracts:
   - Name (line starting with "Name :")
   - Roll Number (from patterns like `RollNo`, `Roll No`)
   - SGPA (from lines containing `SGPA : x.xx`)

---

## 📦 Requirements


### System Packages (must be installed manually)

1. Tesseract OCR
Required for text extraction from scanned PDFs and images.

Windows:
Download Tesseract installer and install.
Add the Tesseract installation path to the system PATH or set it in the script:
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

Linux (Debian/Ubuntu):
sudo apt-get install tesseract-ocr

MacOS (Homebrew):
brew install tesseract


2. Poppler
Required for converting PDFs to images (for OCR).

Windows:
Download Poppler for Windows.
Extract it (e.g., C:\poppler-xx\bin) and add the /bin folder to your PATH.

Linux (Debian/Ubuntu):
sudo apt-get install poppler-utils

MacOS (Homebrew):
brew install poppler


### Python 3.7+ Libraries
Create a virtual environment (recommended) and install dependencies:

pip install -r requirements.txt
