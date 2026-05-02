import streamlit as st
import os

from utils.helpers import clean_text, extract_email, extract_phone
from src.parser import extract_text_from_file
from src.advisor import get_resume_analysis

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
    api_key_input = st.text_input("Google API Key (Optional if set in .env)", type="password")
    if api_key_input:
        os.environ["GOOGLE_API_KEY"] = api_key_input
        
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
            
            # 4. Pure AI Analysis
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                st.error("⚠️ Google API Key is missing. Please add it in the sidebar or `.env` file.")
                st.stop()
            
            analysis_result = get_resume_analysis(cleaned_text, clean_text(job_description) if job_description else "")
            
            if analysis_result["error"]:
                st.error(f"Error during analysis: {analysis_result['error']}")
                st.stop()
                
            data = analysis_result["data"]
            match_score = data.get("match_score", 0)
            skills = data.get("skills", {})
            entities = data.get("entities", {})
            feedback = data.get("feedback", {})

            st.success("Analysis Complete!")
            
            # --- Display Results ---
            st.markdown("---")
            
            # Top row for score and basic info
            score_col, info_col = st.columns([1, 2])
            
            with score_col:
                if job_description:
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
                present_skills = skills.get("present", [])
                if present_skills:
                    # Using pills/tags format
                    html_skills = " ".join([f"<span style='background-color:#E5E7EB; padding: 4px 8px; border-radius: 4px; margin: 2px; display: inline-block;'>{s}</span>" for s in present_skills])
                    st.markdown(html_skills, unsafe_allow_html=True)
                else:
                    st.write("No specific tech skills matched.")
                    
                lacked_skills = skills.get("lacked", [])
                if lacked_skills:
                    st.markdown("#### Lacked Skills")
                    html_lacked = " ".join([f"<span style='background-color:#FEE2E2; color:#991B1B; padding: 4px 8px; border-radius: 4px; margin: 2px; display: inline-block;'>{s}</span>" for s in lacked_skills])
                    st.markdown(html_lacked, unsafe_allow_html=True)
                    
            with ent_col2:
                st.subheader("Entities Detected")
                st.write("**Organizations/Universities:**")
                st.write(", ".join(entities.get("organizations", [])) if entities.get("organizations") else "None found")
                st.write("**Locations:**")
                st.write(", ".join(entities.get("locations", [])) if entities.get("locations") else "None found")
                st.write("**Job Titles:**")
                st.write(", ".join(entities.get("job_titles", [])) if entities.get("job_titles") else "None found")
                
            # AI Feedback section
            st.markdown("---")
            st.subheader("🤖 AI Advisor Feedback")
            
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                st.markdown("#### Strengths 💪")
                for s in feedback.get("strengths", []):
                    st.write(f"- {s}")
                
                st.markdown("#### Weaknesses 📉")
                for w in feedback.get("weaknesses", []):
                    st.write(f"- {w}")
            
            with f_col2:
                st.markdown("#### Suggestions for Improvement 💡")
                for s in feedback.get("suggestions", []):
                    st.write(f"- {s}")
                    
            # Expander for raw text
            with st.expander("View Raw Extracted Text"):
                st.text(raw_text)
