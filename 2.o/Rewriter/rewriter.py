# import os
# import google.generativeai as genai
#
# # -----------------------------
# # 🔹 Configure Gemini
# # -----------------------------
# GEMINI_API_KEY = "AIzaSyDlSBmOxlgPKZJz2okjzlBJS3vDs_KDELk"
# genai.configure(api_key=GEMINI_API_KEY)
#
# # -----------------------------
# # 🔹 Helper Functions
# # -----------------------------
#
# def load_ner_data(file_path):
#     ner_data = {}
#     with open(file_path, "r", encoding="utf-8") as f:
#         for line in f:
#             if ":" in line:
#                 key, value = line.strip().split(":", 1)
#                 value = value.strip().strip("[]").replace("'", "").split(", ")
#                 ner_data[key.strip()] = [v.strip() for v in value if v.strip()]
#     return ner_data
#
# def load_text(file_path):
#     with open(file_path, "r", encoding="utf-8") as f:
#         return f.read()
#
# def extract_sentences(parsed_text):
#     return [line.strip() for line in parsed_text.split("\n") if line.strip()]
#
# def find_skill_gaps(cv_skills, jd_skills):
#     return list(set([s.lower() for s in jd_skills]) - set([s.lower() for s in cv_skills]))
#
# # -----------------------------
# # 🔹 Gemini LLM Functions
# # -----------------------------
#
# def gemini_infer(prompt):
#     """Call Gemini LLM to generate response"""
#     model = genai.GenerativeModel("models/gemini-2.5-flash")
#     response = model.generate_content(prompt)
#     return response.text.strip()
#
# def infer_project_skills(project_sentence):
#     prompt = f"""
#     Identify technical skills and tools inherently required to complete the following project.
#     Output as a comma-separated list.
#     Project description: "{project_sentence}"
#     """
#     skills_text = gemini_infer(prompt)
#     return [s.strip() for s in skills_text.split(",") if s.strip()]
#
# def rewrite_project_sentence(project_sentence, cv_skills, inferred_skills):
#     combined_skills = list(set(cv_skills + inferred_skills))
#     prompt = f"""
#     Rewrite the following resume sentence to highlight relevant skills for ATS.
#     Include these skills naturally: {', '.join(combined_skills)}
#     Original sentence: "{project_sentence}"
#     """
#     rewritten_text = gemini_infer(prompt)
#     return rewritten_text
#
# # -----------------------------
# # 🔹 Main Rewriter Function
# # -----------------------------
#
# def enhance_resume(cv_ner_file, jd_ner_file, cv_parsed_file, jd_parsed_file,
#                    cv_extracted_file, jd_extracted_file, output_report):
#
#     cv_ner = load_ner_data(cv_ner_file)
#     jd_ner = load_ner_data(jd_ner_file)
#
#     cv_parsed_text = load_text(cv_parsed_file)
#     jd_parsed_text = load_text(jd_parsed_file)
#     cv_extracted_text = load_text(cv_extracted_file)
#     jd_extracted_text = load_text(jd_extracted_file)
#
#     project_sentences = extract_sentences(cv_parsed_text)
#
#     cv_skills = cv_ner.get("SKILLS", [])
#     jd_skills = jd_ner.get("SKILLS", [])
#
#     enhanced_projects = []
#     for sentence in project_sentences:
#         inferred_skills = infer_project_skills(sentence)
#         enhanced_sentence = rewrite_project_sentence(sentence, cv_skills, inferred_skills)
#         enhanced_projects.append(enhanced_sentence)
#
#     missing_skills = find_skill_gaps(cv_skills, jd_skills)
#
#     with open(output_report, "w", encoding="utf-8") as f:
#         f.write("Enhanced Project/Experience Sentences:\n")
#         f.write("=====================================\n")
#         for s in enhanced_projects:
#             f.write(f"- {s}\n")
#         f.write("\nSkills Missing in CV (from JD):\n")
#         f.write("=====================================\n")
#         for s in missing_skills:
#             f.write(f"- {s}\n")
#
#     print(f"✅ Resume enhancement complete. Report saved at: {output_report}")
#
# # -----------------------------
# # 🔹 MAIN EXECUTION
# # -----------------------------
#
# if __name__ == "__main__":
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     cv_ner_file = os.path.join(script_dir,'..', "NER_output_CV", "ner_structured_output.txt")
#     jd_ner_file = os.path.join(script_dir,'..', "NER_output_JD", "ner_structured_output.txt")
#     cv_parsed_file = os.path.join(script_dir,'..', "preprocessing_output_CV", "no_stopwords_text_2.o.txt")
#     jd_parsed_file = os.path.join(script_dir,'..', "preprocessing_output_JD", "no_stopwords_text_2.o.txt")
#     cv_extracted_file = os.path.join(script_dir,'..', "preprocessing_output_CV", "extracted_text.txt")
#     jd_extracted_file = os.path.join(script_dir,'..', "preprocessing_output_JD", "extracted_text.txt")
#     output_report = os.path.join(script_dir, "Resume_Enhancement_Report.txt")
#
#     enhance_resume(cv_ner_file, jd_ner_file, cv_parsed_file, jd_parsed_file,
#                    cv_extracted_file, jd_extracted_file, output_report)
#



import os
import google.generativeai as genai

# -----------------------------
# 🔹 Configure Gemini
# -----------------------------
GEMINI_API_KEY = "AIzaSyDlSBmOxlgPKZJz2okjzlBJS3vDs_KDELk"
genai.configure(api_key=GEMINI_API_KEY)

# -----------------------------
# 🔹 Helper Functions
# -----------------------------

def load_ner_data(file_path):
    ner_data = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                key, value = line.strip().split(":", 1)
                value = value.strip().strip("[]").replace("'", "").split(", ")
                ner_data[key.strip()] = [v.strip() for v in value if v.strip()]
    return ner_data

def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_sentences(parsed_text):
    return [line.strip() for line in parsed_text.split("\n") if line.strip()]

def find_skill_gaps(cv_skills, jd_skills):
    return list(set([s.lower() for s in jd_skills]) - set([s.lower() for s in cv_skills]))

# -----------------------------
# 🔹 Gemini LLM Functions
# -----------------------------

# def gemini_infer(prompt):
#     """Call Gemini LLM to generate response"""
#     model = genai.GenerativeModel("models/gemini-2.5-flash")
#     response = model.generate_content(prompt)
#     return response.text.strip()



def gemini_infer(prompt):
    """Call Gemini LLM to generate response with safety guardrails"""

    system_instructions = """
You are an AI assistant inside a Resume Enhancement & NER-Based Matching System.
STRICT RULES (Must Follow):

1. NO HALLUCINATIONS:
   - Do NOT add any new achievements, companies, job roles, dates, metrics, projects, or tools unless they exist in:
       (a) CV parsed text
       (b) CV extracted text
       (c) NER extracted skills
       (d) Inferred project-skill mapping
   - If uncertain, respond with: "Not enough information to infer."

2. SKILLS USAGE RULE:
   - Only skills from the provided skill lists may be inserted.
   - Do NOT create new skills or certifications.
   - If a skill doesn't fit naturally, skip it.

3. JD ALIGNMENT RULE:
   - When rewriting, improve clarity, ATS score, and keyword matching.
   - But NEVER fabricate experience or exaggerate roles.

4. SENTENCE REWRITE RULES:
   - Keep the meaning same as original CV sentence.
   - Only enhance wording and integrate allowed skills.
   - No fictional responsibilities or tools.

5. NER SAFETY RULE:
   - When asked to identify skills, extract ONLY from text.
   - Do NOT invent unseen technologies or frameworks.

6. OUTPUT FORMAT:
   - Respond only with the rewritten text or skill list.
   - No explanations, no extra narrative.

This system is used for a 4th-year B.Tech Major Project. Maintain high accuracy and reliability.
"""

    model = genai.GenerativeModel(
        "models/gemini-2.5-flash",
        system_instruction=system_instructions
    )

    response = model.generate_content(prompt)
    return response.text.strip()




def infer_project_skills(project_sentence):
    prompt = f"""
    Identify technical skills and tools inherently required to complete the following project.
    Output as a comma-separated list.
    Project description: "{project_sentence}"
    """
    skills_text = gemini_infer(prompt)
    return [s.strip() for s in skills_text.split(",") if s.strip()]

def rewrite_project_sentence(project_sentence, cv_skills, inferred_skills):
    combined_skills = list(set(cv_skills + inferred_skills))
    prompt = f"""
    Rewrite the following resume sentence to highlight relevant skills for ATS.
    Include these skills naturally: {', '.join(combined_skills)}
    Original sentence: "{project_sentence}"
    """
    rewritten_text = gemini_infer(prompt)
    return rewritten_text

# -----------------------------
# 🔹 Main Rewriter Function
# -----------------------------

def enhance_resume(cv_ner_file, jd_ner_file, cv_parsed_file, jd_parsed_file,
                   cv_extracted_file, jd_extracted_file, output_report):

    cv_ner = load_ner_data(cv_ner_file)
    jd_ner = load_ner_data(jd_ner_file)

    cv_parsed_text = load_text(cv_parsed_file)
    jd_parsed_text = load_text(jd_parsed_file)
    cv_extracted_text = load_text(cv_extracted_file)
    jd_extracted_text = load_text(jd_extracted_file)

    project_sentences = extract_sentences(cv_parsed_text)

    cv_skills = cv_ner.get("SKILLS", [])
    jd_skills = jd_ner.get("SKILLS", [])

    enhanced_projects = []
    for sentence in project_sentences:
        inferred_skills = infer_project_skills(sentence)
        enhanced_sentence = rewrite_project_sentence(sentence, cv_skills, inferred_skills)
        enhanced_projects.append(enhanced_sentence)

    missing_skills = find_skill_gaps(cv_skills, jd_skills)

    with open(output_report, "w", encoding="utf-8") as f:
        f.write("Enhanced Project/Experience Sentences:\n")
        f.write("=====================================\n")
        for s in enhanced_projects:
            f.write(f"- {s}\n")
        f.write("\nSkills Missing in CV (from JD):\n")
        f.write("=====================================\n")
        for s in missing_skills:
            f.write(f"- {s}\n")

    print(f"✅ Resume enhancement complete. Report saved at: {output_report}")

# -----------------------------
# 🔹 MAIN EXECUTION
# -----------------------------

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cv_ner_file = os.path.join(script_dir, "NER_output_CV", "ner_structured_output.txt")
    jd_ner_file = os.path.join(script_dir, "NER_output_JD", "ner_structured_output.txt")
    cv_parsed_file = os.path.join(script_dir, "preprocessing_output_CV", "no_stopwords_text_2.o.txt")
    jd_parsed_file = os.path.join(script_dir, "preprocessing_output_JD", "no_stopwords_text_2.o.txt")
    cv_extracted_file = os.path.join(script_dir, "preprocessing_output_CV", "extracted_text.txt")
    jd_extracted_file = os.path.join(script_dir, "preprocessing_output_JD", "extracted_text.txt")
    output_report = os.path.join(script_dir, "Resume_Enhancement_Report.txt")

    enhance_resume(cv_ner_file, jd_ner_file, cv_parsed_file, jd_parsed_file,
                   cv_extracted_file, jd_extracted_file, output_report)



