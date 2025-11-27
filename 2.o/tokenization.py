import spacy
import os

# Load spaCy small English model for tokenization
nlp = spacy.load("en_core_web_trf")

def tokenize_text(text):
    """Tokenize text using spaCy while preserving important technical terms."""
    doc = nlp(text)
    tokens = []
    for token in doc:
        # Skip spaces and punctuation
        if token.is_space or token.is_punct:
            continue
        # Keep hyphenated or joined words intact (like scikit-learn, tensorflow)
        tokens.append(token.text)
    return tokens


if __name__ == "__main__":
    input_file = os.path.join("preprocessing_output_CV", "normalized_text.txt")
    output_dir = "preprocessing_output_CV"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "tokens_2.o.txt")

    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    tokens = tokenize_text(text)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(tokens))

    print(f"✅ Tokens saved to '{output_file}'")
