import spacy
import os

def parse_tokens(input_path, output_dir):
    # Load English model
    nlp = spacy.load("en_core_web_trf")

    # Read tokens
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # If tokens are space-separated, join them into a sentence
    # (so spaCy can parse them grammatically)
    if "\n" in text:
        text = " ".join(text.splitlines())

    # Process text through spaCy
    doc = nlp(text)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "parsed_output_2.o.txt")
#   output_path = os.path.join(output_dir, "parsed_output.txt")

    with open(output_path, "w", encoding="utf-8") as f:
        for token in doc:
            f.write(f"{token.text}\t{token.pos_}\t{token.dep_}\t{token.head.text}\n")

    print(f"✅ Parsing complete. Output saved at {output_path}")


if __name__ == "__main__":
    parse_tokens(
#        "preprocessing_output_CV/tokens.txt",
        "preprocessing_output_CV/tokens_2.o.txt",
        "preprocessing_output_CV"
    )
