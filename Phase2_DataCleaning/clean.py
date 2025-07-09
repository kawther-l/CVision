import os
import json
import re
import nltk
from nltk.corpus import stopwords

# Download stopwords if not already available
nltk.download('stopwords')

# === Paths ===
input_folder = os.path.join("..", "Phase1_DataExtraction", "extracted_outputs")
output_folder = "cleaned_outputs"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# === Load stopwords ===
stop_words = set(stopwords.words('english'))

# === Cleaning function ===
def clean_text(text):
    # Lowercase
    text = text.lower()

    # Remove special characters, digits, and multiple spaces
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    # Remove stopwords
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]

    return " ".join(filtered_words)

# === Processing each file ===
print(f"🔍 Looking for files in: {os.path.abspath(input_folder)}\n")

for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        input_path = os.path.join(input_folder, filename)

        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            raw_text = data.get("raw_text", "")

            cleaned_text = clean_text(raw_text)

            # Prepare output
            output_data = {
                "filename": filename,
                "cleaned_text": cleaned_text
            }

            output_path = os.path.join(output_folder, filename)
            with open(output_path, "w", encoding="utf-8") as out_f:
                json.dump(output_data, out_f, indent=2)

            print(f"✅ Cleaned and saved: {filename}")

print("\n🎉 Phase 2 completed! Cleaned text saved in 'cleaned_outputs/' folder.")