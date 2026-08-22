import streamlit as st
from pypdf import PdfReader

from job_analyzer import analyze_job_description
from candidate_analyzer import analyze_candidate
from matching_engine import calculate_skill_match


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="PreHier",
    page_icon="🎯",
    layout="centered"
)

if "job_profile" not in st.session_state:
    st.session_state.job_profile = None

if "candidate_profiles" not in st.session_state:
    st.session_state.candidate_profiles = {}

if "match_results" not in st.session_state:
    st.session_state.match_results = {}


# -----------------------------
# Header
# -----------------------------

st.title("🎯 PreHier")
st.subheader("AI-Powered Pre-Hire Screening")

st.write(
    "Screen and shortlist candidates based on your job requirements."
)

st.divider()


# -----------------------------
# Job Description
# -----------------------------

st.header("💼 Job Description")

job_description = st.text_area(
    "Paste the job description here",
    placeholder="Paste the job description of the role you are hiring for...",
    height=250
)


# -----------------------------
# Analyze Job Description
# -----------------------------


if job_description:

    if st.button("Analyze Job Description"):

        with st.spinner("Analyzing job description..."):

            st.session_state.job_profile = analyze_job_description(
                job_description
            )

        st.subheader("💼 Job Profile")

        st.json(st.session_state.job_profile)


st.divider()


# -----------------------------
# Candidate Resumes
# -----------------------------

st.header("📄 Candidate Resumes")

resumes = st.file_uploader(
    "Upload candidate resumes",
    type=["pdf"],
    accept_multiple_files=True,
    help="Upload one or more candidate resumes in PDF format."
)


# -----------------------------
# Analyze Candidates
# -----------------------------

if resumes:

    st.success(
        f"{len(resumes)} candidate resume(s) uploaded."
    )

    for resume in resumes:

        st.divider()

        st.subheader(f"📄 {resume.name}")

        # Extract resume text
        reader = PdfReader(resume)

        resume_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                resume_text += text + "\n"


        # Show extracted text
        with st.expander("View Extracted Resume Text"):

            st.text_area(
                "Resume Content",
                resume_text,
                height=250,
                key=f"text_{resume.name}"
            )


        # Analyze candidate
        if st.button(
            f"Analyze {resume.name}",
            key=f"analyze_{resume.name}"
        ):

            with st.spinner(
                f"Analyzing {resume.name}..."
            ):

                candidate_profile = analyze_candidate(
                    resume_text
                )

                st.session_state.candidate_profiles[
                    resume.name
                ] = candidate_profile


            # Candidate profile
            st.subheader("👤 Candidate Profile")

            st.json(candidate_profile)


            # Skill matching
            if st.session_state.job_profile:

                result = calculate_skill_match(
                    st.session_state.job_profile["required_skills"],
                    candidate_profile["skills"]
                )
                st.session_state.match_results[
                    resume.name
                ] = result


                st.subheader("🎯 Skill Match")

                st.write(
                    f"Match Score: **{result['score']}%**"
                )


                st.write("### Matched Skills")

                if result["matched_skills"]:
                    st.write(
                        result["matched_skills"]
                    )
                else:
                    st.write("No required skills matched.")


                st.write("### Missing Skills")

                if result["missing_skills"]:
                    st.write(
                        result["missing_skills"]
                    )
                else:
                    st.write(
                        "No required skills are missing."
                    )