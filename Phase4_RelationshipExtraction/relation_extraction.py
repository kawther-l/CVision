import os
import json
import re

# === Paths ===
input_folder = os.path.join("..", "Phase3_EntityRecognition", "entity_outputs")
output_folder = "relationship_outputs"
os.makedirs(output_folder, exist_ok=True)

# === Known Tunisian Cities for City Matching ===
VALID_CITIES = {
    "tunis", "bizerte", "sousse", "sfax", "gabes", "nabeul", "beja",
    "tataouine", "tozeur", "kairouan", "gafsa", "kasserine", "medenine",
    "monastir", "kebili", "mahdia", "manouba", "siliana", "zaghouan",
    "ariana", "ben arous", "jendouba"
}

# === Utility Functions ===

def clean_text(text):
    """Removes unwanted Unicode characters and extra spaces."""
    return re.sub(r"[«»\n\t]+", " ", text).strip()

def parse_location_string(loc_str):
    """
    Parses a location string into structured city + country dict.
    Accepts "Bizerte, Tunisia", "Tunisia", or just "Bizerte".
    """
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

def infer_relationships(data):
    relationships = []
    job_titles = data.get("job_titles", [])
    locations = data.get("locations", [])
    degrees = data.get("degrees", [])
    institutions = data.get("education_institutions", [])
    certs = [clean_text(c.lower()) for c in data.get("certifications", [])]
    skills = [clean_text(s.lower()) for s in data.get("skills", [])]

    # === Job ↔ Location relationships ===
    for title in job_titles:
        if locations:
            for loc in locations:
                parsed = parse_location_string(loc)
                relationships.append({
                    "type": "job_in_location",
                    "job_title": title,
                    "location": parsed
                })
        elif institutions:
            # Trying to extract city from institution if no locations exist
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

    # === Degree ↔ Institution relationships ===
    matched_pairs = set()
    for degree in degrees:
        clean_degree = clean_text(degree)
        for inst in institutions:
            clean_inst = clean_text(inst)
            if (clean_degree, clean_inst) not in matched_pairs:
                relationships.append({
                    "type": "degree_from",
                    "degree": clean_degree,
                    "institution": clean_inst
                })
                matched_pairs.add((clean_degree, clean_inst))

    # === Certification ↔ Skill relationships ===
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
