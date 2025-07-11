import os
import re
import json
import spacy
from datetime import datetime

# Load the small English NLP model from spaCy
nlp = spacy.load("en_core_web_sm")

# Define input/output paths
input_folder = os.path.join("..", "Phase2_DataCleaning", "cleaned_outputs")
output_folder = "entity_outputs"
os.makedirs(output_folder, exist_ok=True)

# === Configuration Lists ===

# Known Tunisian locations (used to validate extracted locations)
VALID_LOCATIONS = {
    "tunis", "bizerte", "sousse", "sfax", "gabes", "nabeul", "beja",
    "tataouine", "tozeur", "kairouan", "gafsa", "kasserine", "medenine",
    "monastir", "kebili", "mahdia", "manouba", "siliana", "zaghouan",
    "ariana", "ben arous", "jendouba", "tunisia"
}

# Regex pattern to match degree phrases (e.g., "Bachelor of Science")
DEGREE_PATTERN = r"(bachelor(?:’s|s)? of [\w\s&]+|master(?:’s|s)? of [\w\s&]+|phd(?: in [\w\s&]+)?)"

# Keywords to help detect educational institutions
INSTITUTION_KEYWORDS = ["university", "institute", "faculty", "school", "college", "academy"]

# Predefined job roles to match from the resume text
JOB_TITLE_KEYWORDS = [
    "data scientist", "data analyst", "software engineer", "developer", "project manager",
    "system administrator", "hr manager", "marketing manager", "technical support", "it engineer",
    "business analyst", "cloud engineer", "frontend developer", "backend developer", "network engineer"
]

# Languages to identify in the text
LANGUAGE_KEYWORDS = [
    "arabic", "english", "french", "german", "spanish", "italian", "russian", "chinese"
]

# Common technical or professional certifications
CERTIFICATION_KEYWORDS = [
    "aws certified", "google cloud certified", "azure certified", "scrum master",
    "ccna", "ccnp", "pmp", "comptia", "microsoft certified", "oracle certified", "cissp", "cyberops"
]

# Patterns to detect emails, phone numbers, links, and years
EMAIL_PATTERN = r'\b[\w\.-]+@[\w\.-]+\.\w+\b'
PHONE_PATTERN = r'\b(?:\+?216)?[\s\(]*[2-9][0-9]{1}[\s\)]*[-\s]?[0-9]{3}[-\s]?[0-9]{3,4}\b'
LINK_PATTERN = r"(https?:\/\/(?:www\.)?(?:linkedin\.com|github\.com)\/[^\s]+)"
YEAR_RANGE_PATTERN = r"\b(19|20)\d{2}\b"

# === Extraction Functions ===

# Extract the name from the top 3 lines of the resume (heuristic)
def extract_name(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines[:3]:
        words = line.split()
        if len(words) in [2, 3] and all(w[0].isupper() for w in words if len(w) > 1):
            return line
    return ""

# Find degrees based on regex pattern
def extract_degrees(text):
    return list({match.title() for match in re.findall(DEGREE_PATTERN, text.lower())})

# Identify educational institutions based on keywords (e.g., "University")
def extract_universities(text):
    institutions = set()
    for line in text.splitlines():
        if any(kw in line.lower() for kw in INSTITUTION_KEYWORDS):
            if not re.search(r"\d{4}", line.lower()):
                institutions.add(line.replace("«", "").replace("»", "").strip().title())
    return list(institutions)

# Use spaCy's noun chunking to extract potential skill phrases dynamically
def extract_skills(text):
    doc = nlp(text)
    skills = set()
    for chunk in doc.noun_chunks:
        if 1 < len(chunk.text) < 50:
            skills.add(chunk.text.strip().title())
    return sorted(skills)

# Extract locations and filter them using the VALID_LOCATIONS set
def extract_locations(doc):
    locations = set()
    for ent in doc.ents:
        loc = ent.text.strip().title()
        if loc.lower() in VALID_LOCATIONS:
            locations.add(loc)
        elif loc.lower() == "tunisia":
            locations.add("Tunisia")
    return sorted(locations)

# Match job titles from the known list
def extract_job_titles(text):
    return sorted({title.title() for title in JOB_TITLE_KEYWORDS if title in text.lower()})

# Match spoken/written languages using simple keyword search
def extract_languages(text):
    return sorted({lang.title() for lang in LANGUAGE_KEYWORDS if lang in text.lower()})

# Match certifications using keyword search
def extract_certifications(text):
    return sorted({cert.title() for cert in CERTIFICATION_KEYWORDS if cert in text.lower()})

# Match links to GitHub or LinkedIn
def extract_links(text):
    return re.findall(LINK_PATTERN, text.lower())

# Estimate number of years of experience based on years found near "experience" section
def estimate_experience_years(text):
    experience_keywords = ["experience", "work history", "employment", "professional background"]
    lines = text.splitlines()
    experience_block = ""

    for idx, line in enumerate(lines):
        if any(kw in line.lower() for kw in experience_keywords):
            experience_block = "\n".join(lines[idx:idx + 15])
            break

    if not experience_block:
        return None

    years = [int("".join(y)) for y in re.findall(r'\b((19|20)\d{2})\b', experience_block)]
    if len(years) < 2:
        return None

    min_year = min(years)
    max_year = min(max(years), datetime.now().year)

    return max_year - min_year if max_year > min_year else None

# Try to extract a professional summary from the top of the document
def extract_summary(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    ignore_keywords = ["experience", "education", "skills", "projects", "contact", "certifications"]

    for i in range(min(10, len(lines))):
        line = lines[i]
        if len(line.split()) >= 25 and not any(kw in line.lower() for kw in ignore_keywords):
            return line
    return None

# === Main Loop: Process each cleaned resume and extract entities ===

for filename in os.listdir(input_folder):
    if not filename.endswith(".json"):
        continue

    with open(os.path.join(input_folder, filename), "r", encoding="utf-8") as f:
        data = json.load(f)
        raw_text = data.get("raw_text", "")

        doc = nlp(raw_text)

        # Collect all extracted data into a structured dictionary
        output = {
            "filename": filename,
            "name": extract_name(raw_text),
            "locations": extract_locations(doc),
            "education_institutions": extract_universities(raw_text),
            "degrees": extract_degrees(raw_text),
            "emails": list(set(re.findall(EMAIL_PATTERN, raw_text))),
            "phones": list(set(re.findall(PHONE_PATTERN, raw_text))),
            "skills": extract_skills(raw_text),
            "job_titles": extract_job_titles(raw_text),
            "languages_spoken": extract_languages(raw_text),
            "certifications": extract_certifications(raw_text),
            "links": extract_links(raw_text),
            "experience_years": estimate_experience_years(raw_text),
            "summary": extract_summary(raw_text)
        }

        # Save the output JSON for this file
        with open(os.path.join(output_folder, filename), "w", encoding="utf-8") as out_f:
            json.dump(output, out_f, indent=2)

        print(f"✅ Processed: {filename}")

print("\n🎯 Enhanced entity recognition complete — results saved in 'entity_outputs/'")
