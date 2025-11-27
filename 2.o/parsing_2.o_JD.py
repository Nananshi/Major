import wordninja
import os

def tokenize_text(text):
    """Tokenize text using wordninja."""
    tokens = wordninja.split(text)
    return tokens

if __name__ == "__main__":
    input_file = os.path.join("preprocessing_output_JD", "normalized_text.txt")
    output_dir = "preprocessing_output_JD"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "tokens_2.o.txt")

    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    tokens = tokenize_text(text)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(tokens))

    print(f"✅ Tokens saved to '{output_file}'")
