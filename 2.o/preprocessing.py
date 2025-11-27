# text extractor
# normalization
# stop word removal
# tokenization

from text_extractor import extract_text_from_pdf
from normalization import normalize_text
from stop_word_removal import remove_stopwords
from tokenization import tokenize_text

pdf_path = "1.pdf"

text = extract_text_from_pdf(pdf_path)
text = normalize_text(text)
text = remove_stopwords(text)
tokens = tokenize_text(text)

print(tokens[:50])
