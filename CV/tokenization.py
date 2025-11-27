from nltk.tokenize import word_tokenize

def tokenize(text):
    return word_tokenize(text)

tokenized_text = tokenize(txt)
with open("1(tokenized).txt", 'w', encoding="utf-8") as f:
    f.write(' '.join(tokenized_text))
