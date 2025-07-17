import os
import json
import re

# === Input/Output Directories ===
input_folder = os.path.join("..", "Phase3_EntityRecognition", "entity_outputs")
output_folder = "relationship_outputs"
os.makedirs(output_folder, exist_ok=True)

# === Valid Tunisian Cities for Location Parsing ===
VALID_CITIES = {
    "tunis", "bizerte", "sousse", "sfax", "gabes", "nabeul", "beja",
    "tataouine", "tozeur", "kairouan", "gafsa", "kasserine", "medenine",
    "monastir", "kebili", "mahdia", "manouba", "siliana", "zaghouan",
    "ariana", "ben arous", "jendouba"
}

# === Clean and Parse Utilities ===

def clean_text(text):
    """Cleans stray characters from text like « » and whitespace."""
    return re.sub(r"[«»\n\t]+", " ", text).strip()

def parse_location_string(loc_str):
    """Converts strings like 'Sfax, Tunisia' to structured {'city': ..., 'country': ...}."""
    loc_str = loc_str.strip().title()
    parts = [p.strip() for p in loc_str.split(",")]

    if len(parts) == 2:
        return {"city": parts[0], "country": parts[1]}
    elif loc_str.lower() in VALID_CITIES:
        return {"city": loc_str, "country": "Tunisia"}
    elif loc_str == "Tunisia":
        return {"city": None, "country": "Tunisia"}
    else:
        return {"city": None, "country": loc_str}

# === Relationship Extraction Logic ===

def infer_relationships(data):
    relationships = []

    # Extract data
    job_titles = data.get("job_titles", [])
    locations = data.get("locations", [])
    degrees = data.get("degrees", [])
    institutions = data.get("education_institutions", [])
    certs = [clean_text(c.lower()) for c in data.get("certifications", [])]
    skills = [clean_text(s.lower()) for s in data.get("skills", [])]

    # — Job ↔ Location
    for title in job_titles:
        if locations:
            for loc in locations:
                parsed = parse_location_string(loc)
                relationships.append({
                    "type": "job_in_location",
                    "job_title": title,
                    "location": parsed
                })
        else:
            for inst in institutions:
                for city in VALID_CITIES:
                    if city in inst.lower():
                        relationships.append({
                            "type": "job_in_location",
                            "job_title": title,
                            "location": {
                                "city": city.title(),
                                "country": "Tunisia"
                            }
                        })

    # — Degree ↔ Institution
    matched_pairs = set()
    for degree in degrees:
        for inst in institutions:
            pair = (degree, inst)
            if pair not in matched_pairs:
                relationships.append({
                    "type": "degree_from",
                    "degree": clean_text(degree),
                    "institution": clean_text(inst)
                })
                matched_pairs.add(pair)

    # — Certification ↔ Skill
    for cert in certs:
        for skill in skills:
            if cert in skill or skill in cert:
                relationships.append({
                    "type": "certification_for_skill",
                    "certification": cert.title(),
                    "skill": skill.title()
                })

    return relationships

# === Main Loop ===

for filename in os.listdir(input_folder):
    if not filename.endswith(".json"):
        continue

    with open(os.path.join(input_folder, filename), "r", encoding="utf-8") as f:
        data = json.load(f)

    rels = infer_relationships(data)

    output = {
        "filename": filename,
        "relationships": rels
    }

    with open(os.path.join(output_folder, filename), "w", encoding="utf-8") as out_f:
        json.dump(output, out_f, indent=2)

    print(f"✅ Relationships extracted: {filename}")

print("\n🔗 Phase 4 complete — Smart relationships saved to 'relationship_outputs'")
