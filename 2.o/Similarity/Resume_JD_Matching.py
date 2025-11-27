import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# 🔹 Helper Functions
# -----------------------------

def load_ner_data(file_path):
    """Load structured NER data from file and convert to dictionary."""
    ner_data = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                key, value = line.strip().split(":", 1)
                value = value.strip().strip("[]").replace("'", "").split(", ")
                ner_data[key.strip()] = [v.strip() for v in value if v.strip()]
    return ner_data

def calculate_cosine_similarity(list1, list2):
    """Calculate cosine similarity between two lists of words (for skills/experience)."""
    if not list1 or not list2:
        return 0.0
    text1 = " ".join(list1)
    text2 = " ".join(list2)
    vectorizer = CountVectorizer().fit([text1, text2])
    vectors = vectorizer.transform([text1, text2])
    similarity = cosine_similarity(vectors)[0][1]
    return round(similarity * 100, 2)

def calculate_education_similarity(cv_list, jd_list):
    """Set-based similarity for EDUCATION using JD as reference."""
    set_cv = set(cv_list)
    set_jd = set(jd_list)
    if not set_cv or not set_jd:
        return 0.0
    overlap = set_cv.intersection(set_jd)
    similarity = len(overlap) / len(set_jd)  # % of JD degrees matched
    return round(similarity * 100, 2)

def get_match_category(percentage):
    """Convert numeric percentage to descriptive category."""
    if percentage <= 40:
        return "Poor"
    elif percentage <= 60:
        return "Ok"
    elif percentage <= 80:
        return "Good"
    else:
        return "Very Good"

# -----------------------------
# 🔹 Normalization Functions
# -----------------------------

# Education normalization
education_map = {
    "b.tech": "bachelor",
    "btech": "bachelor",
    "m.tech": "master",
    "mtech": "master",
    "bachelor": "bachelor",
    "master": "master",
    "phd": "phd",
    "bsc": "bachelor",
    "msc": "master",
    "university": "university"  # optional
}

def normalize_education(degrees):
    normalized = []
    for deg in degrees:
        deg_lower = deg.lower()
        for key, val in education_map.items():
            if key in deg_lower:
                normalized.append(val)
                break
        else:
            normalized.append(deg_lower)
    return normalized

def normalize_skills(skills):
    return [skill.lower() for skill in skills]

def normalize_experience(exp):
    return [e.lower() for e in exp]

# -----------------------------
# 🔹 Main Matching Function
# -----------------------------

def match_resume_jd(cv_file, jd_file):
    """Compare CV and JD NER outputs; score based on skills, experience, education."""

    output_dir = os.path.dirname(os.path.abspath(__file__))

    cv_data = load_ner_data(cv_file)
    jd_data = load_ner_data(jd_file)

    # Fields and weights
    fields = ["SKILLS", "EXPERIENCE", "EDUCATION", "PROJECTS", "ACHIEVEMENTS"]
    weighted_fields = {"SKILLS": 0.5, "EXPERIENCE": 0.3, "EDUCATION": 0.2}

    match_scores = {}
    weighted_score = 0.0

    for field in fields:
        cv_field = cv_data.get(field, [])
        jd_field = jd_data.get(field, [])

        # Apply normalization
        if field == "EDUCATION":
            cv_field = normalize_education(cv_field)
            jd_field = normalize_education(jd_field)
            similarity = calculate_education_similarity(cv_field, jd_field)
        elif field == "SKILLS":
            cv_field = normalize_skills(cv_field)
            jd_field = normalize_skills(jd_field)
            similarity = calculate_cosine_similarity(cv_field, jd_field)
        elif field == "EXPERIENCE":
            cv_field = normalize_experience(cv_field)
            jd_field = normalize_experience(jd_field)
            similarity = calculate_cosine_similarity(cv_field, jd_field)
        else:
            similarity = calculate_cosine_similarity(cv_field, jd_field)

        match_scores[field] = similarity

        if field in weighted_fields:
            weighted_score += similarity * weighted_fields[field]

    overall_match = round(weighted_score, 2)

    # Save detailed report
    output_file = os.path.join(output_dir, "Resume_JD_Match_Report.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Resume–JD Matching Report\n")
        f.write("===========================\n\n")
        for field, score in match_scores.items():
            category = get_match_category(score)
            f.write(f"{field} Match: {score}% → {category}\n")
        f.write("\n")
        f.write("Final Scoring Basis: Skills (50%), Experience (30%), Education (20%)\n")
        overall_category = get_match_category(overall_match)
        f.write(f"\nOverall Match Score: {overall_match}% → {overall_category}\n")

    # Save overall score to a separate file
    score_file = os.path.join(output_dir, "score.txt")
    with open(score_file, "w", encoding="utf-8") as sf:
        sf.write(str(overall_match))

    # Print summary
    print("✅ Resume–JD Matching Complete!")
    print(f"📄 Report saved to: {output_file}")
    print(f"📄 Overall match score saved to: {score_file}")
    print("\n📊 Field-wise Scores:")
    for field, score in match_scores.items():
        category = get_match_category(score)
        print(f"  {field}: {score}% → {category}")

    overall_category = get_match_category(overall_match)
    print(f"\n🎯 Weighted Overall Match: {overall_match}% → {overall_category}")

    return match_scores, overall_match

# -----------------------------
# 🔹 MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    cv_file = os.path.join("..", "NER_output_CV", "ner_structured_output.txt")
    jd_file = os.path.join("..", "NER_output_JD", "ner_structured_output.txt")

    match_resume_jd(cv_file, jd_file)
