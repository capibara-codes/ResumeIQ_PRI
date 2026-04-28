import spacy

# Try to load the model, fallback to a message if not found.
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading en_core_web_sm model...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str) -> dict:
    """
    Extracts basic entities from the resume text using spaCy.
    Since we are not fine-tuning yet, we'll rely on the base model
    and simple rule-based extractions.
    """
    doc = nlp(text)
    
    entities = {
        "PERSON": set(),
        "ORG": set(),       # Companies, universities
        "GPE": set(),       # Locations
        "DATE": set(),      # Dates/Years
    }
    
    for ent in doc.ents:
        if ent.label_ in entities:
            # Basic cleaning
            cleaned_ent = ent.text.strip().replace('\n', ' ')
            if len(cleaned_ent) > 2: # Filter out noise
                entities[ent.label_].add(cleaned_ent)
            
    # Convert sets back to lists for easier serialization later
    return {k: list(v) for k, v in entities.items()}

# Basic list of tech skills to look for using keyword matching as a fallback
# until a custom NER model is trained.
COMMON_SKILLS = [
    "python", "java", "javascript", "c++", "c#", "ruby", "php", "swift", "kotlin",
    "sql", "mysql", "postgresql", "mongodb", "aws", "azure", "gcp", "docker",
    "kubernetes", "react", "angular", "vue", "django", "flask", "spring", "node.js",
    "html", "css", "git", "machine learning", "deep learning", "nlp", "pandas",
    "numpy", "scikit-learn", "tensorflow", "pytorch", "excel", "agile", "scrum"
]

def extract_skills(text: str) -> list[str]:
    """
    Rule-based skill extraction.
    """
    text_lower = text.lower()
    found_skills = []
    
    for skill in COMMON_SKILLS:
        # Simple whole word matching
        if f"\\b{skill}\\b" in text_lower or f" {skill} " in text_lower or text_lower.startswith(f"{skill} ") or text_lower.endswith(f" {skill}"):
             found_skills.append(skill.title())
             
    # A slightly better way using regex:
    import re
    found_skills_regex = []
    for skill in COMMON_SKILLS:
        # Escape skill for regex
        escaped_skill = re.escape(skill)
        pattern = r'\b' + escaped_skill + r'\b'
        if re.search(pattern, text_lower):
            found_skills_regex.append(skill.title())
            
    return found_skills_regex
