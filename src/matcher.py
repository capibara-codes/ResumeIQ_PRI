from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text: str, job_description: str) -> float:
    """
    Calculates the cosine similarity between the resume text and the job description
    using TF-IDF vectorization.
    Returns a score between 0 and 100.
    """
    if not resume_text or not job_description:
        return 0.0

    documents = [resume_text, job_description]
    
    # Initialize TF-IDF Vectorizer
    # stop_words='english' removes common words like 'and', 'the', 'is'
    vectorizer = TfidfVectorizer(stop_words='english')
    
    try:
        # Fit and transform the documents
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        # Calculate cosine similarity between the first document (resume) 
        # and the second document (job description)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        
        # Extract the score (it's a 2D array) and convert to percentage
        match_score = similarity[0][0] * 100
        return round(match_score, 2)
    except Exception as e:
        print(f"Error calculating match score: {e}")
        return 0.0
