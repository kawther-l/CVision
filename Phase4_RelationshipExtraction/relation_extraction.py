import json
import os
import re
from collections import defaultdict
from difflib import SequenceMatcher

# I used this function to measure how similar two strings are.
# It helps detect soft matches between job titles, skills, and degrees.
def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# This is the main function that processes all resume JSON files to extract relationships.
def rel_all(input_folder: str, output_folder: str) -> None:
    """
    For each enhanced JSON resume file, this function extracts potential relationships
    between degrees, skills, and job titles, such as skill-to-job and degree-to-job mappings.

    Args:
        input_folder (str): Path to the folder containing enhanced JSON resume files.
        output_folder (str): Path to the folder where relationship-enhanced JSON files will be saved.
    """
    # I make sure the output directory exists before saving any files
    os.makedirs(output_folder, exist_ok=True)

    # Loop through each JSON resume file in the input directory
    for filename in os.listdir(input_folder):
        if not filename.endswith('.json'):
            continue

        input_path = os.path.join(input_folder, filename)
        with open(input_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # I extract relevant fields that can have logical relationships
        skills = data.get("skills", [])
        job_titles = data.get("job_titles", [])
        degree_titles = data.get("degree_titles", [])
        degree_types = data.get("degree_types", [])

        # I will store the relationships here
        relationships = {
            "skill_to_job": [],
            "degree_to_job": []
        }

        # I match each skill with job titles to see which skills relate to which roles
        for skill in skills:
            for job in job_titles:
                if similar(skill, job) > 0.4 or skill.lower() in job.lower() or job.lower() in skill.lower():
                    relationships["skill_to_job"].append({"skill": skill, "job_title": job})

        # I match degrees (titles and types) to job titles similarly
        for degree in degree_titles + degree_types:
            for job in job_titles:
                if similar(degree, job) > 0.4 or degree.lower() in job.lower() or job.lower() in degree.lower():
                    relationships["degree_to_job"].append({"degree": degree, "job_title": job})

        # I embed the extracted relationships back into the resume JSON
        data["relationships"] = relationships
        data["relationships_count"] = len(relationships["skill_to_job"]) + len(relationships["degree_to_job"])

        # I save the enhanced JSON with relationships added
        output_path = os.path.join(output_folder, filename)
        with open(output_path, "w", encoding="utf-8") as out_file:
            json.dump(data, out_file, indent=4, ensure_ascii=False)

        print(f"[✔] Relationships extracted for {filename}")
