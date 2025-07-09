# Phase 2: Data Cleaning – CVision Project

This phase focuses on cleaning and normalizing raw resume text that was extracted in Phase 1. The goal is to prepare high-quality, structured text for the next steps, such as entity recognition and data extraction.

## 🔍 What was done

- Loaded JSON files containing raw text from the `Phase1_DataExtraction/extracted_outputs/` folder.
- Applied text cleaning techniques including:
  - Lowercasing all text
  - Removing special characters, numbers, and symbols
  - Removing stopwords using NLTK
  - Normalizing whitespace and formatting
- Cleaned text was saved into new JSON files inside the `cleaned_outputs/` folder.

## 🛠️ Tools & Libraries

- Python
- `re` (Regex) – for text normalization
- `nltk` – for stopword removal
- `json` and `os` – for file handling

## ✅ Output

Each file will contain:
```json
{
"filename": "CV_FILENAME.pdf.json",
"cleaned_text": "normalized and stopword-free text..."
}