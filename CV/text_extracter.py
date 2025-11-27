import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Example usage:
folder = "resumes"
all_texts = {}
for file in os.listdir(folder):
    if file.endswith(".pdf"):
        path = os.path.join(folder, file)
        text = extract_text_from_pdf(path)
        all_texts[file] = text

print(list(all_texts.keys())[:5])  # show first 5 files
print(all_texts[list(all_texts.keys())[0]][:500])  # preview first 500 chars
