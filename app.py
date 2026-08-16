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

    st.header("🎯 Interview Type")

    interview_type = st.selectbox(
        "What type of interview do you want to practice?",
        [
            "Technical",
            "Behavioral",
            "Mixed"
        ]
    )

    st.write(f"Selected interview type: **{interview_type}**")


    from groq_helper import ask_groq

    if st.button("Test AI"):
        response = ask_groq("Say hello")
        st.write(response)