import re
import spacy
from parser.utils import load_skills_list

nlp = spacy.load("en_core_web_sm")

EDU_KEYWORDS = [
    'bachelor', 'master', 'b.tech', 'm.tech', 'phd', 
    'diploma', 'high school', 'college', 'university'
]

EXPERIENCE_SECTIONS = ['experience', 'work experience', 'professional experience', 'personal projects']

def extract_email(text):
    emails = re.findall(r'\b[\w.-]+@[\w.-]+\.\w+\b', text)
    return emails[0] if emails else None

def extract_phone(text):
    cleaned_text = text.replace('\n', ' ').replace('\r', ' ')
    candidates = re.findall(r'\d{10,15}', cleaned_text)
    
    if candidates:
        return candidates[0]
    
    return None

def extract_name(text):
    doc = nlp(text)
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    if name:
        name = re.sub(r'\d+', '', name)
        name = re.sub(r'[^a-zA-Z\s.-]', '', name)
        name = re.sub(r'[-_]+$', '', name)
        name = name.strip()

    return name

def extract_education(text):
    edu_list = []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        for kw in EDU_KEYWORDS:
            if kw.lower() in line.lower():
                edu_list.append(line)
                break
    return edu_list

def extract_skills(text):
    skills_db = load_skills_list()
    text_lower = text.lower()
    skills = [skill for skill in skills_db if skill.lower() in text_lower]
    return skills

def extract_experience(text):
    """
    Extracts Experience or Personal Projects section.
    Returns a list of clean lines, merges broken lines if necessary.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    full_text = "\n".join(lines)

    pattern = re.compile(
        r"(Experience|Work Experience|Professional Experience|Personal Projects)(.*?)(Education|Skills|Projects|Certifications|Achievements|$)",
        re.DOTALL | re.IGNORECASE
    )
    match = pattern.search(full_text)
    if match:
        experience_block = match.group(2).strip()
    else:
        return []


    exp_lines = []
    buffer = ""
    for line in experience_block.split("\n"):
        if line.strip() == "":
            continue
        if re.match(r'^[•\-\d]', line):
            if buffer:
                exp_lines.append(buffer.strip())
            buffer = re.sub(r'^[•\-\d\s]+', '', line)
        else:
            if buffer:
                buffer += " " + line
            else:
                buffer = line
    if buffer:
        exp_lines.append(buffer.strip())

    return exp_lines

def parse_resume(text):
    return {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Education": extract_education(text),
        "Skills": extract_skills(text),
        "Experience": extract_experience(text)
    }
