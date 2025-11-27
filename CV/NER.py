import spacy

# Load best spaCy model
nlp = spacy.load("en_core_web_trf")

# === Step 1: Read text from your file ===
with open("1(tokenized).txt", "r", encoding="utf-8") as f:
    text = f.read()

# === Step 2: Clean text ===
text = " ".join(text.split())

# === Step 3: Run NER ===
doc = nlp(text)

# === Step 4: Organize detected entities ===
structured_data = {}
for ent in doc.ents:
    label = ent.label_
    structured_data.setdefault(label, set()).add(ent.text)

# === Step 5: Define skill and experience keyword sets ===
# (You can expand these as needed)
SKILL_KEYWORDS = {
    "python", "java", "c++", "tensorflow", "keras", "scikit learn", "machine learning",
    "deep learning", "nlp", "sql", "power bi", "excel", "tableau", "data science"
}

EXPERIENCE_KEYWORDS = {
    "internship", "project", "experience", "developer", "engineer", "worked", "research", "built"
}

# === Step 6: Add custom entities ===
structured_data["SKILLS"] = set()
structured_data["EXPERIENCE"] = set()

if "PRODUCT" in structured_data:
    for prod in structured_data["PRODUCT"]:
        clean_prod = prod.lower()
        if any(skill in clean_prod for skill in SKILL_KEYWORDS):
            structured_data["SKILLS"].add(prod)
        elif any(exp in clean_prod for exp in EXPERIENCE_KEYWORDS):
            structured_data["EXPERIENCE"].add(prod)

# === Step 7: Convert sets to lists ===
structured_data = {k: list(v) for k, v in structured_data.items()}

# === Step 8: Print results ===
print("\n=== Structured NER Dictionary (Refined) ===")
for key, values in structured_data.items():
    print(f"{key}: {values}")
