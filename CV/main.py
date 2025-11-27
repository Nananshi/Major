import fitz  # PyMuPDF
import nltk
import string
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import os

# Download necessary resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Load SpaCy model for NER
nlp = spacy.load("en_core_web_sm")

# === 1️⃣ PDF TEXT EXTRACTION ===
def extract_text_from_pdf(pdf_path, output_file="extracted_text.txt"):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[1] Extracted text saved as {output_file}")
    return text

# === 2️⃣ NORMALIZATION (Lowercasing) ===
def normalize_text(text, output_file="normalized_text.txt"):
    normalized = text.lower()
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(normalized)
    print(f"[2] Normalized text saved as {output_file}")
    return normalized

# === 3️⃣ PUNCTUATION REMOVAL ===
def remove_punctuation(text, output_file="no_punctuation.txt"):
    cleaned = text.translate(str.maketrans("", "", string.punctuation))
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned)
    print(f"[3] Text without punctuation saved as {output_file}")
    return cleaned

# === 4️⃣ TOKENIZATION ===
def tokenize_text(text, output_file="tokens.txt"):
    tokens = word_tokenize(text)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(" ".join(tokens))
    print(f"[4] Tokens saved as {output_file}")
    return tokens

# === 5️⃣ STOPWORD REMOVAL ===
def remove_stopwords(tokens, output_file="no_stopwords.txt"):
    stop_words = set(stopwords.words('english'))
    filtered = [w for w in tokens if w.lower() not in stop_words]
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(" ".join(filtered))
    print(f"[5] Stopwords removed and saved as {output_file}")
    return filtered

# === 6️⃣ POS TAGGING ===
def pos_tagging(tokens, output_file="pos_tags.txt"):
    tags = pos_tag(tokens)
    with open(output_file, "w", encoding="utf-8") as f:
        for word, tag in tags:
            f.write(f"{word}/{tag} ")
    print(f"[6] POS tagging saved as {output_file}")
    return tags

# === 7️⃣ NAMED ENTITY RECOGNITION ===
def named_entity_recognition(text, output_file="ner_output.txt"):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    with open(output_file, "w", encoding="utf-8") as f:
        for ent, label in entities:
            f.write(f"{ent} --> {label}\n")
    print(f"[7] Named Entities saved as {output_file}")
    return entities

# === MAIN PIPELINE ===
def full_pipeline(pdf_path, output_dir="Outputs"):
    os.makedirs(output_dir, exist_ok=True)

    extracted = extract_text_from_pdf(pdf_path, os.path.join(output_dir, "extracted_text.txt"))
    normalized = normalize_text(extracted, os.path.join(output_dir, "normalized_text.txt"))
    no_punct = remove_punctuation(normalized, os.path.join(output_dir, "no_punctuation.txt"))
    tokens = tokenize_text(no_punct, os.path.join(output_dir, "tokens.txt"))
    no_stop = remove_stopwords(tokens, os.path.join(output_dir, "no_stopwords.txt"))
    pos_tags = pos_tagging(no_stop, os.path.join(output_dir, "pos_tags.txt"))
    entities = named_entity_recognition(" ".join(no_stop), os.path.join(output_dir, "ner_output.txt"))

    print("\n✅ Pipeline completed successfully.")
    print(f"All outputs saved in: {os.path.abspath(output_dir)}")

# === Run Example ===
if __name__ == "__main__":
    pdf_input = r"C:\Users\HP\OneDrive\Desktop\Major\sample_resume.pdf"  # 🔹 replace with your file path
    full_pipeline(pdf_input)
