from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_text(text):
    """Basic cleaning to help TF-IDF"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def calculate_match_score(resume_skills: list, jd_skills: list) -> float:
    """
    Improved version: Compare list of skills rather than long paragraphs.
    """
    if not resume_skills or not jd_skills:
        return 0.0

    # Convert lists back to strings for the vectorizer
    resume_str = " ".join(resume_skills)
    jd_str = " ".join(jd_skills)
    
    documents = [resume_str, jd_str]
    vectorizer = TfidfVectorizer()
    
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        
        # Boost the score
        # Cosine similarity is mathematically conservative. 
        # For resumes, a 0.3 (30%) is often actually a good match.
        # We can apply a multiplier or a non-linear scaling to make it "human-readable"
        raw_score = similarity[0][0]
        
        # Scaling logic: Make the score feel more like a grading system
        adjusted_score = (raw_score ** 0.5) * 100 
        
        return round(min(adjusted_score, 100.0), 2)
    except Exception as e:
        return 0.0