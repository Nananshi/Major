import re
import os

def normalize_text(text):
    """Clean text by removing special characters and extra spaces."""
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\-\(\)]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

if __name__ == "__main__":
    input_file = os.path.join("preprocessing_output_CV", "extracted_text.txt")
    output_dir = "preprocessing_output_CV"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "normalized_text.txt")

    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    normalized = normalize_text(text)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(normalized)

    print(f"✅ Normalized text saved to '{output_file}'")
