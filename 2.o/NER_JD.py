import spacy
import ast
import os
import re

# -----------------------------
# 🔹 Load spaCy transformer model
# -----------------------------
nlp = spacy.load("en_core_web_trf")

# -----------------------------
# 🔹 Keyword Dictionaries
# -----------------------------
SKILL_KEYWORDS = {
    "python", "java", "c++", "machine learning", "deep learning", "data science",
    "sql", "power bi", "excel", "pandas", "numpy", "matplotlib", "seaborn",
    "tensorflow", "keras", "pytorch", "nlp", "transformers", "scikit-learn",
    "flask", "django", "fastapi", "aws", "azure", "git", "github", "linux"
}

EXPERIENCE_KEYWORDS = {
    "internship", "project", "developed", "engineer", "research",
    "experience", "worked", "implemented", "analyzed", "designed", "built",
    "maintained", "tested", "collaborated", "led"
}

PROJECT_KEYWORDS = {
    "project", "developed", "created", "built", "designed",
    "implemented", "prototype", "application"
}

ACHIEVEMENT_KEYWORDS = {
    "award", "certification", "certificate", "achievement", "honor",
    "recognition", "rank", "won", "secured", "completed", "participated"
}

EDU_KEYWORDS = {
    "b.tech", "m.tech", "bachelor", "master", "phd",
    "university", "college", "institute"
}


def extract_project_names(text):
    """
    Extract potential project names from text.
    Detects phrases after project-related keywords like
    'project', 'developed', 'built', 'created', etc.
    """
    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)

    # Regex patterns for different cases
    patterns = [
        r'(?:project\s+(?:titled|named|called)?\s*)([A-Z][\w\s\-]{2,50})',  # after 'project'
        r'(?:developed\s+(?:an|a|the)?\s*)([A-Z][\w\s\-]{2,50})',           # after 'developed'
        r'(?:built\s+(?:an|a|the)?\s*)([A-Z][\w\s\-]{2,50})',               # after 'built'
        r'(?:created\s+(?:an|a|the)?\s*)([A-Z][\w\s\-]{2,50})',             # after 'created'
        r'(?:designed\s+(?:an|a|the)?\s*)([A-Z][\w\s\-]{2,50})'             # after 'designed'
    ]

    names = set()
    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        for match in matches:
            cleaned = match.strip().title()
            # Avoid adding generic words like "Project Application"
            if len(cleaned.split()) > 1:
                names.add(cleaned)
    return names


# -----------------------------
# 🔹 Main Function
# -----------------------------
def perform_full_ner(input_file, output_dir="NER_output_JD"):
    """Perform NER + keyword extraction from tokens file."""

    # Read tokens
    with open(input_file, "r", encoding="utf-8") as f:
        data = f.read()

    try:
        tokens = ast.literal_eval(data)
    except Exception as e:
        print("⚠️ Error reading token list:", e)
        return

    text = " ".join(tokens).lower()

    # Process text with spaCy
    doc = nlp(text)

    # Create structure
    structured_data = {
        "NAME": set(),
        "ORG": set(),
        "EDUCATION": set(),
        "EXPERIENCE": set(),
        "PROJECTS": set(),
        "ACHIEVEMENTS": set(),
        "SKILLS": set()
    }

    # --- Named Entity Recognition Extraction ---
    for ent in doc.ents:
        label = ent.label_
        if label == "PERSON":
            structured_data["NAME"].add(ent.text)
        elif label == "ORG":
            structured_data["ORG"].add(ent.text)
        elif label in ["EDUCATION", "FAC"]:
            structured_data["EDUCATION"].add(ent.text)
        elif label in ["WORK_OF_ART", "PRODUCT"]:
            structured_data["PROJECTS"].add(ent.text)

    # --- Keyword-based detection ---
    for skill in SKILL_KEYWORDS:
        if skill in text:
            structured_data["SKILLS"].add(skill)

    for exp_word in EXPERIENCE_KEYWORDS:
        if exp_word in text:
            structured_data["EXPERIENCE"].add(exp_word)

    for proj_word in PROJECT_KEYWORDS:
        if proj_word in text:
            structured_data["PROJECTS"].add(proj_word)

    for ach_word in ACHIEVEMENT_KEYWORDS:
        if ach_word in text:
            structured_data["ACHIEVEMENTS"].add(ach_word)

    for edu_word in EDU_KEYWORDS:
        if edu_word in text:
            structured_data["EDUCATION"].add(edu_word)

    # --- Extract potential project names ---
    project_names = extract_project_names(text)
    structured_data["PROJECTS"].update(project_names)

    # Convert sets to sorted lists
    structured_data = {k: sorted(list(v)) for k, v in structured_data.items()}

    # Prepare output folder
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "ner_structured_output.txt")

    # Save structured data
    with open(output_file, "w", encoding="utf-8") as out:
        for k, v in structured_data.items():
            out.write(f"{k}: {v}\n")

    print(f"✅ NER + Keyword extraction complete.")
    print(f"📄 Structured output saved at: {output_file}")

    # Optional: show a quick summary
    for k, v in structured_data.items():
        print(f"{k}: {len(v)} items")

    return structured_data


# -----------------------------
# 🔹 Run Script
# -----------------------------
if __name__ == "__main__":
    input_path = os.path.join("preprocessing_output_JD", "tokens.txt")
    perform_full_ner(input_path)
