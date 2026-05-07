from typing import Tuple, Optional
import os

import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import PyPDF2
import google.generativeai as genai

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CareerCraft",
    layout="wide",
    page_icon="📄"
)

# ─────────────────────────────────────────────────────────────
# LOAD ENV VARIABLES
# ─────────────────────────────────────────────────────────────
load_dotenv()

# ─────────────────────────────────────────────────────────────
# GET API KEY
# ─────────────────────────────────────────────────────────────
def get_api_key() -> Optional[str]:
    try:
        return (
            st.secrets.get("GEMINI_API_KEY")
            or os.getenv("GEMINI_API_KEY")
        )
    except Exception:
        return os.getenv("GEMINI_API_KEY")

API_KEY = get_api_key()

if not API_KEY:
    st.error("❌ GEMINI_API_KEY not found.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=API_KEY)

# ─────────────────────────────────────────────────────────────
# GEMINI MODEL SETUP
# ─────────────────────────────────────────────────────────────
MODEL_NAME = "gemini-2.5-flash-lite"

try:
    model = genai.GenerativeModel(MODEL_NAME)

    st.success(f"✅ Using Gemini Model: {MODEL_NAME}")

except Exception as e:
    st.error("❌ Failed to initialize Gemini.")
    st.exception(e)
    st.stop()

# ─────────────────────────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────────────────────────
def load_and_resize(path: str, size: Tuple[int, int]):
    try:
        img = Image.open(path)
        return img.resize(size)
    except Exception:
        return None

def safe_show_image(path: str, size: Tuple[int, int]):
    img = load_and_resize(path, size)

    if img:
        st.image(img)

def input_pdf_text(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

        return text

    except Exception as e:
        st.error("❌ Error reading PDF.")
        st.exception(e)
        return ""

def truncate(text: str, max_chars: int):
    if len(text) > max_chars:
        return text[:max_chars]

    return text

# ─────────────────────────────────────────────────────────────
# GEMINI RESPONSE
# ─────────────────────────────────────────────────────────────
def get_gemini_response(prompt: str):
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.6,
                "max_output_tokens": 1200,
            }
        )

        return response.text

    except Exception as e:
        st.error("⚠️ Gemini request failed.")
        st.exception(e)
        return "Gemini request failed."

# ─────────────────────────────────────────────────────────────
# UI — HEADER
# ─────────────────────────────────────────────────────────────
intro_col, img_col = st.columns([3, 1])

with intro_col:
    st.title("🎯 CareerCraft")
    st.header("AI-Powered ATS Resume Analyzer")

    st.markdown("""
    CareerCraft helps job seekers optimize resumes for ATS systems.

    Upload your resume and compare it against any job description
    using Google's Gemini AI.
    """)

with img_col:
    safe_show_image("images/icon_dashboard.png", (200, 200))

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# FEATURES
# ─────────────────────────────────────────────────────────────
offer_img, offer_text = st.columns([1, 2])

with offer_img:
    safe_show_image("images/offerings.png", (180, 180))

with offer_text:
    st.subheader("🚀 Features")

    st.markdown("""
    - ATS Resume Analysis
    - Skill Gap Detection
    - Keyword Optimization
    - Resume Matching Score
    - AI Generated Suggestions
    - Personalized Profile Summary
    """)

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# MAIN ATS ANALYZER
# ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Analyze Your Resume")

    job_desc = st.text_area(
        "Paste Job Description",
        height=180
    )

    uploaded_resume = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    if st.button("🔍 Analyze Resume"):

        if not job_desc:
            st.warning("Please enter a job description.")

        elif not uploaded_resume:
            st.warning("Please upload your resume.")

        else:
            with st.spinner("Analyzing Resume..."):

                resume_text = input_pdf_text(uploaded_resume)

                if not resume_text.strip():
                    st.warning("Could not extract text from PDF.")

                else:
                    jd_text = truncate(job_desc, 7000)
                    cv_text = truncate(resume_text, 9000)

                    prompt = f"""
                    You are an ATS Resume Analyzer.

                    Compare the resume with the job description.

                    Provide:

                    1. ATS Match Percentage
                    2. Missing Keywords
                    3. Strengths
                    4. Weaknesses
                    5. Improvement Suggestions
                    6. Professional Summary

                    JOB DESCRIPTION:
                    {jd_text}

                    RESUME:
                    {cv_text}
                    """

                    response = get_gemini_response(prompt)

                    st.markdown("## 📊 Analysis Result")
                    st.write(response)

with col2:
    safe_show_image("images/analysis.png", (250, 180))

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# FAQ SECTION
# ─────────────────────────────────────────────────────────────
faq_col1, faq_col2 = st.columns(2)

with faq_col1:
    safe_show_image("images/faq.png", (200, 200))

with faq_col2:
    st.subheader("❓ FAQ")

    st.write("### What is CareerCraft?")
    st.write("An AI-powered ATS resume analyzer.")

    st.write("### Is my data stored?")
    st.write("No. Uploaded resumes are not stored.")

    st.write("### Which AI model is used?")
    st.write(f"Google Gemini ({MODEL_NAME})")

    st.write("### Can I deploy this project?")
    st.write("Yes. Fork the repo and deploy on Streamlit Cloud.")

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style='text-align: center;'>

    ### 👨‍💻 Developed by Siddharath Negi

    CareerCraft — AI Resume Analyzer

    </div>
    """,
    unsafe_allow_html=True
)