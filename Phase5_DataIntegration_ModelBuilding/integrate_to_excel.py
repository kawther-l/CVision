import os
import json
import pandas as pd

# Define paths
entity_folder = os.path.join("..", "Phase3_EntityRecognition", "entity_outputs")
relation_folder = os.path.join("..", "Phase4_RelationshipExtraction", "relation_outputs")
output_folder = "integrated_outputs"
os.makedirs(output_folder, exist_ok=True)

rows = []

# Loop through entity files
for filename in os.listdir(entity_folder):
    if not filename.endswith(".json"):
        continue

    # Load entity data
    with open(os.path.join(entity_folder, filename), "r", encoding="utf-8") as ef:
        entity_data = json.load(ef)

    # Load relationships if available
    relation_path = os.path.join(relation_folder, filename)
    relationships = []
    if os.path.exists(relation_path):
        with open(relation_path, "r", encoding="utf-8") as rf:
            rel_data = json.load(rf)
            relationships = rel_data.get("relationships", [])

    # Prepare row
    row = {
        "filename": filename,
        "name": entity_data.get("name", ""),
        "emails": ", ".join(entity_data.get("emails", [])),
        "phones": ", ".join(entity_data.get("phones", [])),
        "degrees": ", ".join(entity_data.get("degrees", [])),
        "institutions": ", ".join(entity_data.get("education_institutions", [])),
        "skills": ", ".join(entity_data.get("skills", [])),
        "job_titles": ", ".join(entity_data.get("job_titles", [])),
        "locations": ", ".join(entity_data.get("locations", [])),
        "certifications": ", ".join(entity_data.get("certifications", [])),
        "languages": ", ".join(entity_data.get("languages_spoken", [])),
        "links": ", ".join(entity_data.get("links", [])),
        "experience_years": entity_data.get("experience_years", ""),
        "summary": entity_data.get("summary", ""),
        "relationships_count": len(relationships)
    }

    rows.append(row)

# Convert to DataFrame
df = pd.DataFrame(rows)

# Export to Excel and CSV
excel_path = os.path.join(output_folder, "CVision_Integrated.xlsx")
csv_path = os.path.join(output_folder, "CVision_Integrated.csv")

df.to_excel(excel_path, index=False)
df.to_csv(csv_path, index=False)

print(f"✅ Integration complete. Excel saved to: {excel_path}")
