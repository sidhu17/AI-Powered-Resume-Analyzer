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

# ─────────────────────────────────────────────────────────────
# CONFIGURE GEMINI
# ─────────────────────────────────────────────────────────────
genai.configure(api_key=API_KEY)

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
def safe_show_image(path: str, width=None):
    try:
        img = Image.open(path)
        st.image(img, width=width)
    except Exception:
        pass

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
                "temperature": 0.4,
                "max_output_tokens": 1500,
            }
        )

        return response.text

    except Exception as e:
        st.error("⚠️ Gemini request failed.")
        st.exception(e)
        return "Gemini request failed."

# ─────────────────────────────────────────────────────────────
# HEADER SECTION
# ─────────────────────────────────────────────────────────────
intro_col, img_col = st.columns([3, 1.5], vertical_alignment="center")

with intro_col:
    st.title("🎯 CareerCraft")
    st.header("AI-Powered ATS Resume Analyzer")

    st.markdown("""
    CareerCraft helps job seekers optimize resumes for ATS systems.

    Upload your resume and compare it against any job description
    using Google's Gemini AI.
    """)

with img_col:
    st.markdown("<br><br>", unsafe_allow_html=True)
    safe_show_image("images/icon_dashboard.png", width=350)

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# FEATURES SECTION
# ─────────────────────────────────────────────────────────────
offer_img, offer_text = st.columns([1,2], vertical_alignment="center")

with offer_img:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    safe_show_image("images/offerings.png", width=350)

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

col1, col2 = st.columns([1.9, 1], gap="large")

with col1:

    st.subheader("📂 Analyze Your Resume")

    job_desc = st.text_area(
        "Paste Job Description",
        height=120
    )

    uploaded_resume = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    analyze = st.button("🔍 Analyze Resume")

with col2:

    st.markdown("", unsafe_allow_html=True)

    safe_show_image(
        "images/analysis.png",
        width=450
    )

# ─────────────────────────────────────────────────────────────
# RESULT SECTION (OUTSIDE COLUMNS)
# ─────────────────────────────────────────────────────────────

if analyze:

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

                jd_text = truncate(job_desc, 2500)
                cv_text = truncate(resume_text, 3500)

                prompt = f"""
                You are an ATS Resume Analyzer.

                Analyze the resume against the job description.

                Return the response in clean markdown format.

                Use:
                - bullet points
                - short paragraphs

                Sections:
                1. ATS Match Percentage
                2. Missing Skills
                3. Key Strengths
                4. Improvement Suggestions

                Job Description:
                {jd_text}

                Resume:
                {cv_text}
                """

                response = get_gemini_response(prompt)

# FULL WIDTH RESPONSE
st.markdown("---")

if analyze and job_desc and uploaded_resume:

    st.markdown("## 📊 ATS Resume Analyzer Report")
    formatted_response = response.replace("</div>", "")
    st.markdown(
        f"""
        <div style="
            width:100%;
            line-height:1.9;
            font-size:16px;
            overflow-wrap:break-word;
            word-wrap:break-word;
            white-space:normal;
        ">
        {response}
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("---")
# ─────────────────────────────────────────────────────────────
# FAQ SECTION
# ─────────────────────────────────────────────────────────────
faq_col1, faq_col2 = st.columns([0.8,1.0], gap="small")

with faq_col1:
    st.markdown("<br><br>", unsafe_allow_html=True)
    safe_show_image("images/faq.png", width=450)

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

    CareerCraft — AI-powered ATS Resume Analyzer

    </div>
    """,
    unsafe_allow_html=True
)