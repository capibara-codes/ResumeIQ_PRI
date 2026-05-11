import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Missing API Key! Please set GEMINI_API_KEY in Secrets or .env")

def get_resume_analysis(resume_text: str, job_description: str = "") -> dict:
    """
    Sends the resume and optionally the job description to Gemini to get a full analysis.
    Returns a dictionary containing score, skills, entities, and feedback.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"data": None, "error": "Google API Key is missing."}
        
    genai.configure(api_key=api_key)
    
    # Using gemini-2.5-flash with JSON mode enabled
    model = genai.GenerativeModel(
        "gemini-2.5-flash", 
        generation_config={"response_mime_type": "application/json", "temperature": 0.2}
    )
    
    #it is the prompt that we sned to model to get anlysis of resume and job description.
    system_prompt = """
You are an expert technical recruiter and resume analyzer.
You will be provided with a candidate's resume text and optionally a target job description.
You must analyze the resume and return a JSON object with the following exact structure:
{
    "match_score": <int>, // 0 to 100 representing how well the resume fits the job description. If no job description is provided, return 0. Be realistic and critical.
    "skills": {
        "present": ["skill1", "skill2"], // List of technical and soft skills present in the resume
        "lacked": ["skill3"] // List of skills mentioned in the job description that are missing from the resume (empty if no job description)
    },
    "entities": {
        "organizations": ["org1", "org2"], // Companies, universities, or schools the candidate has been part of
        "locations": ["loc1", "loc2"], // Geographic locations mentioned
        "job_titles": ["title1", "title2"] // Roles the candidate has held
    },
    "feedback": {
        "strengths": ["strength1", "strength2"], // Key strong points of the resume
        "weaknesses": ["weakness1", "weakness2"], // Areas where the resume falls short
        "suggestions": ["suggestion1", "suggestion2"] // Actionable advice to improve the resume
    }
}
Categorize entities precisely. Only output valid JSON.
"""

    user_prompt = f"Resume Text:\n{resume_text}\n"
    if job_description:
        user_prompt += f"\nTarget Job Description:\n{job_description}"

    try:
        response = model.generate_content(
            contents=system_prompt + "\n\n" + user_prompt,
        )
        
        result_text = response.text
        analysis_data = json.loads(result_text)
        return {"data": analysis_data, "error": None}
    
    except Exception as e:
        error_msg = str(e)
        return {"data": None, "error": f"Gemini API Error: {error_msg}"}
