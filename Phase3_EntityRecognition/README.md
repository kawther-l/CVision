# Phase 3: Entity Recognition – CVision Project

This phase focuses on extracting structured information from the cleaned resume text using Named Entity Recognition (NER) techniques. The goal is to identify and categorize meaningful data such as names, companies, locations, and dates from resumes to prepare them for further analysis or presentation.

## 🎯 What Was Done

- Loaded cleaned resume data from Phase 2 (`cleaned_outputs/`)
- Applied NER using the **spaCy** NLP library (`en_core_web_sm` model)
- Extracted standard entities:
  - `PERSON` – Names
  - `ORG` – Organizations / Companies
  - `GPE` – Geopolitical Entities (countries, cities)
  - `DATE` – Years or time periods

- Additionally used regex-based **fallback patterns** to detect:
  - Email addresses
  - Phone numbers
  - Dates (for consistency and backup if NER misses them)

- Saved extracted entities to structured JSON files in `entity_outputs/`

## 🛠️ Tools & Libraries

- Python  
- [spaCy](https://spacy.io/) for NER  
- `re` (Regex) for fallback entity detection  
- `json`, `os` for file handling


