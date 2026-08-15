import streamlit as st
from pypdf import PdfReader

st.set_page_config(
    page_title="PreHier",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 PreHier")
st.subheader("AI-Powered Interview Preparation")

st.write(
    "Prepare for your job interview using your resume, "
    "job description, and preferred interview type."
)

st.divider()

st.header("📄 Upload Your Resume")

resume = st.file_uploader(
    "Upload your resume",
    type=["pdf"],
    help="Upload your resume in PDF format."
)

if resume:
    st.success(f"Resume uploaded: {resume.name}")
    reader = PdfReader(resume)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text + "\n"

    st.subheader("📃 Extracted Resume Text")

    st.text_area(
        "Resume content",
        resume_text,
        height=400
    )