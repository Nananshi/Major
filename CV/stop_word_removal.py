import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def remove_stopwords(tokens):
    return [w for w in tokens if w not in stop_words]

# Example usage:
filtered_tokens = remove_stopwords(tokens)
print(filtered_tokens[:50])  # first 50 meaningful words












import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize

# Read the tokenized text
with open("1(tokenized).txt", 'r', encoding='utf-8') as f:
    txt = f.read()

# Convert string back to list of tokens if needed
# If you already saved as Python list string, you can use eval() safely here
tokens = eval(txt)  # converts '[token1, token2, ...]' string back to list

# Load stopwords
stop_words = set(stopwords.words('english'))

# Remove stopwords
def remove_stopwords(tokens):
    return [w for w in tokens if w.lower() not in stop_words]

stop_wordless = remove_stopwords(tokens)

# Save to file
with open("1(stoped_word).txt", 'w', encoding="utf-8') as f:
    f.write(str(stop_wordless))

print(stop_wordless[:50])  # preview first 50 words
