# ResumeIQ - AI-Powered Resume Analyzer & Enhancer

ResumeIQ is an intelligent web application built with Streamlit, spaCy, and OpenAI to help candidates improve their resumes. It parses resumes (PDF/DOCX), extracts key entities and skills, calculates a match score against a target job description, and provides actionable AI-generated feedback.

## Features

- **Document Parsing:** Supports both PDF and DOCX file uploads.
- **Entity Extraction:** Uses NLP (spaCy) to identify skills, organizations, and locations.
- **Job Matching:** Calculates a similarity score (0-100%) between your resume and a target job description using TF-IDF and Cosine Similarity.
- **AI Feedback:** Integrates with OpenAI (GPT-3.5) to analyze the resume and suggest improvements, pointing out strengths and weaknesses.

## Project Structure

```text
ResumeIQ/
├── app.py                 # The main Streamlit web application
├── requirements.txt       # Dependencies
├── .env                   # Environment variables (OpenAI API Key)
├── data/                  # Directory for test PDFs and Job Descriptions
├── models/
│   └── custom_ner/        # Directory for future custom spaCy NER models
├── src/
│   ├── parser.py          # PDF/DOCX parsing logic
│   ├── extractor.py       # spaCy NER and rule-based skill extraction
│   ├── matcher.py         # TF-IDF & Cosine Similarity logic
│   └── advisor.py         # OpenAI API integration
└── utils/
    └── helpers.py         # Text cleaning and regex utilities
```

## Setup & Installation

1. **Clone or Download the Repository:**
   ```bash
   cd ResumeIQ
   ```

2. **Create a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: The app will automatically download the required `spaCy` `en_core_web_sm` model on first run if it isn't already installed.)*

4. **Configure Environment Variables:**
   - Open the `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key.
   - Alternatively, you can input the API key directly in the Streamlit app sidebar.

## Running the Application

Start the Streamlit development server:

```bash
streamlit run app.py
```

The app will open automatically in your default web browser (typically at `http://localhost:8501`).

## How to Use

1. Upload a valid Resume (PDF or DOCX).
2. (Optional) Paste the Target Job Description in the provided text area.
3. Click on **Analyze Resume**.
4. View the match score, extracted entities, and the AI's detailed feedback on how to improve your resume!
