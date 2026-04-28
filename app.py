import streamlit as st
import os

from utils.helpers import clean_text, extract_email, extract_phone
from src.parser import extract_text_from_file
from src.extractor import extract_entities, extract_skills
from src.matcher import calculate_match_score
from src.advisor import get_resume_feedback

# --- Page Configuration ---
st.set_page_config(
    page_title="ResumeIQ - AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stProgress .st-bo {
        background-color: #10B981;
    }
</style>
""", unsafe_allow_html=True)

# --- UI Header ---
st.markdown("<p class='main-header'>ResumeIQ</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>AI-Powered Resume Analyzer & Enhancer</p>", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key_input = st.text_input("OpenAI API Key (Optional if set in .env)", type="password")
    if api_key_input:
        os.environ["OPENAI_API_KEY"] = api_key_input
        
    st.markdown("---")
    st.markdown("### How it works")
    st.markdown("1. Upload your resume (PDF/DOCX).")
    st.markdown("2. (Optional) Paste a Job Description to get a match score.")
    st.markdown("3. Click **Analyze Resume** to see extracted details and AI feedback.")

# --- Main App Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=['pdf', 'docx', 'doc'])

with col2:
    st.subheader("🎯 Target Job Description")
    job_description = st.text_area("Paste job description here for matching (optional)", height=150)

if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
    if not uploaded_file:
        st.error("Please upload a resume first.")
    else:
        with st.spinner("Analyzing your resume..."):
            
            # 1. Parse File
            raw_text = extract_text_from_file(uploaded_file, uploaded_file.name)
            if not raw_text:
                st.error("Could not extract text from the file.")
                st.stop()
                
            # 2. Clean Text
            cleaned_text = clean_text(raw_text)
            
            # 3. Extract Basic Info
            email = extract_email(cleaned_text)
            phone = extract_phone(cleaned_text)
            
            # 4. Extract Entities & Skills
            entities = extract_entities(cleaned_text)
            skills = extract_skills(cleaned_text)
            
            # 5. Match Score
            match_score = None
            if job_description:
                match_score = calculate_match_score(cleaned_text, clean_text(job_description))
                
            # 6. AI Feedback
            api_key = os.getenv("OPENAI_API_KEY")
            feedback_data = None
            if api_key:
                feedback_data = get_resume_feedback(cleaned_text, job_description)
            else:
                st.warning("⚠️ OpenAI API Key is missing. AI Feedback will not be generated. Please add it in the sidebar or `.env` file.")

            st.success("Analysis Complete!")
            
            # --- Display Results ---
            st.markdown("---")
            
            # Top row for score and basic info
            score_col, info_col = st.columns([1, 2])
            
            with score_col:
                if match_score is not None:
                    st.markdown(f"<div class='metric-card'><h3>Match Score</h3><h2>{match_score}%</h2></div>", unsafe_allow_html=True)
                    st.progress(match_score / 100.0)
                else:
                    st.info("Add a Job Description to see match score.")
                    
            with info_col:
                st.subheader("Contact Information")
                st.write(f"**Email:** {email if email else 'Not found'}")
                st.write(f"**Phone:** {phone if phone else 'Not found'}")
                
            st.markdown("---")
            
            # Extraction details
            ent_col1, ent_col2 = st.columns(2)
            with ent_col1:
                st.subheader("Extracted Skills")
                if skills:
                    # Using pills/tags format
                    html_skills = " ".join([f"<span style='background-color:#E5E7EB; padding: 4px 8px; border-radius: 4px; margin: 2px; display: inline-block;'>{s}</span>" for s in set(skills)])
                    st.markdown(html_skills, unsafe_allow_html=True)
                else:
                    st.write("No specific tech skills matched.")
                    
            with ent_col2:
                st.subheader("Entities Detected")
                st.write("**Organizations/Universities:**")
                st.write(", ".join(entities.get("ORG", [])) if entities.get("ORG") else "None found")
                st.write("**Locations:**")
                st.write(", ".join(entities.get("GPE", [])) if entities.get("GPE") else "None found")
                
            # AI Feedback section
            if feedback_data:
                st.markdown("---")
                st.subheader("🤖 AI Advisor Feedback")
                if feedback_data["error"]:
                    st.error(f"Error generating feedback: {feedback_data['error']}")
                else:
                    st.markdown(feedback_data["feedback"])
                    
            # Expander for raw text
            with st.expander("View Raw Extracted Text"):
                st.text(raw_text)
