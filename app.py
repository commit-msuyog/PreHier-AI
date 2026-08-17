import streamlit as st
from pypdf import PdfReader
from groq_helper import ask_groq

st.set_page_config(
    page_title="PreHier",
    page_icon="🎯",
    layout="centered"
)

st.title("PreHier")
st.subheader("AI-Powered Pre-Hire Screening")

st.write(
    "Screen and shortlist candidates based on your job requirements."
)

st.divider()

resumes = st.file_uploader(
    "Upload Candidate Resumes",
    type=["pdf"],
    accept_multiple_files=True,
    help="Upload resumes of candidates in PDF format."
)

if resumes:

    st.success(f"{len(resumes)} candidate resume(s) uploaded")

    for resume in resumes:

        reader = PdfReader(resume)
        resume_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                resume_text += text + "\n"

        with st.expander(resume.name):
            st.text_area(
                "Extracted Resume Text",
                resume_text,
                height=250,
                key=resume.name
            )

    st.subheader("📃 Extracted Resume Text")

    st.text_area(
        "Resume content",
        resume_text,
        height=400
    )

    st.divider()

    st.header("💼 Job Description")

    job_description = st.text_area(
        "Paste the job description here (optional)",
        placeholder="Paste the job description of the role you are applying for...",
        height=250
    )

    if job_description:
        st.success("Job description added")

    st.divider()