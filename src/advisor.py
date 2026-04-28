import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
# It will automatically look for OPENAI_API_KEY in the environment variables
client = OpenAI()

def get_resume_feedback(resume_text: str, job_description: str = "") -> dict:
    """
    Sends the resume and optionally the job description to OpenAI to get feedback.
    Returns a dictionary containing strengths, weaknesses, and suggestions.
    """
    
    # We will use gpt-3.5-turbo as per user preference
    model = "gpt-3.5-turbo"
    
    prompt = f"""
You are an expert technical recruiter and resume reviewer.
Please review the following resume text. 
{f"Also, consider this job description to see how well it fits: {job_description}" if job_description else ""}

Resume Text:
{resume_text}

Provide your analysis in the following format exactly, using Markdown:
### Strengths
- [Strength 1]
- [Strength 2]
...

### Weaknesses
- [Weakness 1]
- [Weakness 2]
...

### Suggestions for Improvement
- [Suggestion 1]
- [Suggestion 2]
...
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful and professional career advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        feedback_text = response.choices[0].message.content
        return {"feedback": feedback_text, "error": None}
    
    except Exception as e:
        return {"feedback": None, "error": str(e)}
