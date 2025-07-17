import os
import json
import pandas as pd

def integrate_all(entity_jsons, relation_jsons, output_dir):
    """
    Merges Phase 3 (entities) and Phase 4 (relationships) into Excel + CSV.
    Args:
        entity_jsons (list): List of Phase 3 JSON file paths.
        relation_jsons (list): List of Phase 4 JSON file paths.
        output_dir (str): Directory where output files will be stored.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Pre-load all relationships into a dictionary
    relation_map = {}
    for rfile in relation_jsons:
        with open(rfile, "r", encoding="utf-8") as rf:
            data = json.load(rf)
            relation_map[data.get("filename", "")] = data.get("relationships", [])

    rows = []

    # Process each entity file and enrich with its relationships
    for efile in entity_jsons:
        with open(efile, "r", encoding="utf-8") as ef:
            entity = json.load(ef)

        filename = entity.get("filename", "")
        rels = relation_map.get(filename, [])

        # Build flat row for spreadsheet
        row = {
            "filename": filename,
            "name": entity.get("name", ""),
            "emails": ", ".join(entity.get("emails", [])),
            "phones": ", ".join(entity.get("phones", [])),
            "degrees": ", ".join(entity.get("degrees", [])),
            "institutions": ", ".join(entity.get("education_institutions", [])),
            "skills": ", ".join(entity.get("skills", [])),
            "job_titles": ", ".join(entity.get("job_titles", [])),
            "locations": ", ".join(entity.get("locations", [])),
            "certifications": ", ".join(entity.get("certifications", [])),
            "languages": ", ".join(entity.get("languages_spoken", [])),
            "links": ", ".join(entity.get("links", [])),
            "experience_years": entity.get("experience_years", ""),
            "summary": entity.get("summary", ""),
            "relationships_count": len(rels)
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    # Output to Excel and CSV
    excel_path = os.path.join(output_dir, "CVision_Integrated.xlsx")
    csv_path = os.path.join(output_dir, "CVision_Integrated.csv")

    df.to_excel(excel_path, index=False)
    df.to_csv(csv_path, index=False)

    return excel_path
