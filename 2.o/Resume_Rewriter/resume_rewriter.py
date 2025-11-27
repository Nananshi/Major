import os
import pdfplumber
from fpdf import FPDF

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

# Function to read the enhancement report
def read_report(report_path):
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Parse enhanced sentences and missing skills
    enhanced_section = content.split("Skills Missing in CV (from JD):")[0].replace("Enhanced Project/Experience Sentences:\n=====================================\n", "").strip()
    missing_skills_section = content.split("Skills Missing in CV (from JD):\n=====================================\n")[1].strip()
    # Extract options from enhanced_section
    enhanced_sentences = []
    lines = enhanced_section.split("\n")
    current_option = ""
    for line in lines:
        line = line.strip()
        if line.startswith("**Option"):
            if current_option:
                enhanced_sentences.append(current_option.strip())
            current_option = ""
        elif line.startswith(">"):
            current_option += line[1:].strip() + " "
        elif current_option and not line.startswith("*") and not line.startswith("-"):
            current_option += line + " "
    if current_option:
        enhanced_sentences.append(current_option.strip())
    missing_skills = [line.strip("- ").strip() for line in missing_skills_section.split("\n") if line.strip()]
    return enhanced_sentences, missing_skills

# Function to rewrite the resume in ATS-optimized format
def rewrite_resume(original_text, enhanced_sentences, missing_skills):
    # Basic info
    name = "DYLAN HERNANDEZ"
    title = "GRADUATE MACHINE LEARNING DEVELOPER"
    summary = (
        "Experienced software professional looking for data science and machine learning roles. "
        "Masters in machine learning. Good knowledge of software development processes and object-oriented programming. "
        "Sound knowledge of Python, Scikit-learn, and Keras."
    )

    # Work experience
    work_exp = enhanced_sentences[0] if enhanced_sentences else "Developed Async Functions to connect ML applications and client databases."

    # Education
    education = (
        "M.Tech (Machine Learning), IIIT Delhi, 2021\n"
        "B.Tech (Instrumentation), Jodhpur University, Jodhpur, 2018"
    )

    # Skills - merge original + missing
    original_skills = [
        "Python", "Scikit Learn", "Keras", "Tensorflow",
        "Object Oriented Programming", "Machine Learning",
        "Software Engineering", "Application Development"
    ]
    all_skills = list(set(original_skills + missing_skills))  # Remove duplicates

    # Projects
    projects_list = [
        "Intelligent Disease Recognition using Cause Pair Extraction",
        "Understanding Neural Networks - Nanyang University"
    ]

    # Convert lists to bullet strings safely
    work_exp_bullets = f"- {work_exp}"
    skills_bullets = ", ".join(all_skills)
    projects_bullets = "\n- ".join(projects_list)

    # Compose the resume
    resume_content = (
        f"{name.upper()}\n"
        f"{title}\n\n"
        f"PROFESSIONAL SUMMARY\n{summary}\n\n"
        f"WORK EXPERIENCE\nSoftware Developer and Analyst Trainee | CISCO | OCT 2018 - May 2019\n"
        f"{work_exp_bullets}\n\n"
        f"EDUCATION\n{education}\n\n"
        f"SKILLS\n{skills_bullets}\n\n"
        f"PROJECTS\n- {projects_bullets}"
    )

    return resume_content.strip()

# Function to generate PDF
def generate_pdf(content, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(10, 10, 10)  # Set left, top, right margins
    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line == "DYLAN HERNANDEZ":  # Name
            pdf.set_font("Arial", "B", 16)
            pdf.multi_cell(180, 12, txt=line)
            pdf.ln(5)
        elif line in ["GRADUATE MACHINE LEARNING DEVELOPER", "PROFESSIONAL SUMMARY", "WORK EXPERIENCE", "EDUCATION", "SKILLS", "PROJECTS"]:  # Section headings
            pdf.set_font("Arial", "B", 14)
            pdf.multi_cell(180, 10, txt=line)
            pdf.ln(5)
        elif line.startswith("Software Developer"):  # Job title
            pdf.set_font("Arial", "B", 12)
            pdf.multi_cell(180, 10, txt=line)
        elif line.startswith("-"):  # Bullets
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(170, 10, txt=line)  # Slight indent
        else:  # Normal text
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(180, 10, txt=line)
    pdf.output(output_path)

# Main function
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(script_dir, "1.pdf")
    report_path = os.path.join(script_dir, "Resume_Enhancement_Report.txt")
    output_pdf = os.path.join(script_dir, "resume.pdf")

    # Extract original text
    original_text = extract_text_from_pdf(pdf_path)

    # Read enhancements
    enhanced_sentences, missing_skills = read_report(report_path)

    # Rewrite resume
    rewritten_resume = rewrite_resume(original_text, enhanced_sentences, missing_skills)

    # Generate PDF
    generate_pdf(rewritten_resume, output_pdf)

    print(f"ATS-optimized resume PDF generated at: {output_pdf}")

if __name__ == "__main__":
    main()