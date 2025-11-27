import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    """Extract raw text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if __name__ == "__main__":
    pdf_path = "ML.pdf"
    output_dir = "preprocessing_output_JD"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "extracted_text.txt")

    text = extract_text_from_pdf(pdf_path)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"✅ Extracted text saved to '{output_file}'")
