import os
import json
import pandas as pd

# This function loads all the enhanced JSON resumes into memory.
# I used this to gather all processed records from Phase 3 or 4.
def load_ner_results(directory):
    records = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            path = os.path.join(directory, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    records.append(data)
            except Exception as e:
                print(f"[Error] Failed to read {file}: {e}")
    return records

# I flatten the nested JSON data into simple key-value pairs so it can be stored in tabular form.
def flatten_record(record):
    return {
        "filename": record.get("filename", ""),
        "name": record.get("name", ""),
        "emails": ", ".join(record.get("emails", [])),
        "phones": ", ".join(record.get("phones", [])),
        "current_location": record.get("current_location", ""),
        "job_titles": ", ".join(record.get("job_titles", [])),
        "experience_years": record.get("experience_years", 0),
        "education_institutions": ", ".join(record.get("education_institutions", [])),
        "degree_types": ", ".join(record.get("degree_types", [])),
        "degree_titles": ", ".join(record.get("degree_titles", [])),
        "languages_spoken": ", ".join(record.get("languages_spoken", [])),
        "certifications": ", ".join(record.get("certifications", [])),
        "summary": record.get("summary", ""),
        "skills": ", ".join(record.get("skills", [])),
        "linkedin": record.get("linkedin", ""),
        "github": record.get("github", ""),
        "relationships_count": record.get("relationships_count", 0)
    }

# This is the main function I use to compile all the structured resume data into an Excel spreadsheet.
def main():
    input_folder = "Phase3_EntityRecognition/output"  # This could be changed to Phase4 output
    output_excel = "Phase5_DataIntegration/final_output.xlsx"

    print(f"🔄 Loading NER results from: {input_folder}")
    raw_data = load_ner_results(input_folder)
    print(f"✅ Loaded {len(raw_data)} records")

    print("📄 Flattening records...")
    flat_data = [flatten_record(record) for record in raw_data]

    # I convert the flattened data into a DataFrame using pandas
    print(f"💾 Writing to Excel: {output_excel}")
    df = pd.DataFrame(flat_data)

    # I ensure the output directory exists before saving
    os.makedirs(os.path.dirname(output_excel), exist_ok=True)
    df.to_excel(output_excel, index=False)

    print("✅ Done! Your structured CV data is ready.")

# I run this script directly when executed as the main file
if __name__ == "__main__":
    main()
