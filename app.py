import streamlit as st

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