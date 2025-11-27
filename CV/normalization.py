import re

def normalize_text(text):
    text = text.lower()
    # Replace newlines and tabs with a space
    text = re.sub(r'[\n\t]', ' ', text)
    # Keep letters and spaces (remove numbers and punctuation)
    text = re.sub(r'[^a-zA-Z ]+', '', text)
    # Collapse multiple spaces into one
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

if __name__ == '__main__':
    normalize_text("extracted_text.txt")