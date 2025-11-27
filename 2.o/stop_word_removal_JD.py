## Before parsing


# import nltk
# from nltk.corpus import stopwords
# import os
#
# nltk.download("stopwords", quiet=True)
#
# def remove_stopwords(text):
#     """Remove English stopwords from text."""
#     words = text.split()
#     stop_words = set(stopwords.words("english"))
#     filtered_words = [word for word in words if word.lower() not in stop_words]
#     return " ".join(filtered_words)
#
# if __name__ == "__main__":
#     input_file = os.path.join("preprocessing_output_JD", "normalized_text.txt")
#     output_dir = "preprocessing_output_JD"
#     os.makedirs(output_dir, exist_ok=True)
#     output_file = os.path.join(output_dir, "no_stopwords_text.txt")
#
#     with open(input_file, "r", encoding="utf-8") as f:
#         text = f.read()
#
#     cleaned_text = remove_stopwords(text)
#
#     with open(output_file, "w", encoding="utf-8") as f:
#         f.write(cleaned_text)
#
#     print(f"✅ Stopword-removed text saved to '{output_file}'")



## After Parsing

import nltk
from nltk.corpus import stopwords
import os

nltk.download("stopwords", quiet=True)


def remove_stopwords(text):
    """Remove English stopwords from parsed text."""
    words = text.split()
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return " ".join(filtered_words)


if __name__ == "__main__":
    # Input: parsed text (after parsing step)
    input_file = os.path.join("preprocessing_output_JD", "parsed_output_2.o.txt")

    # Output directory and file
    output_dir = "preprocessing_output_JD"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "no_stopwords_text_2.o.txt")

    # Read parsed text
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Remove stopwords
    cleaned_text = remove_stopwords(text)

    # Save the stopword-free text
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print(f"✅ Stopword-removed text saved to '{output_file}'")
