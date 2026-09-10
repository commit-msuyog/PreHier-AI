import streamlit as st

from services.screening_service import screen_resume


def show_resume_section(job_profile):

    st.divider()

    st.header("📄 Candidate Resumes")

    resumes = st.file_uploader(
        "Upload candidate resumes",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more candidate resumes in PDF format."
    )

    if not resumes:
        return

    st.success(
        f"{len(resumes)} candidate resume(s) uploaded."
    )

    if st.button(
        "🚀 Analyze All Resumes",
        type="primary"
    ):

        if not job_profile:
            st.warning(
                "Please analyze the job description first."
            )
            return

        st.session_state.candidate_profiles = {}
        st.session_state.match_results = {}

        progress_bar = st.progress(0)
        status_text = st.empty()

        total_resumes = len(resumes)

        for index, resume in enumerate(resumes):

            status_text.write(
                f"Analyzing {resume.name} "
                f"({index + 1}/{total_resumes})..."
            )

            candidate_profile, match_result = screen_resume(
                resume,
                job_profile
            )

            st.session_state.candidate_profiles[
                resume.name
            ] = candidate_profile

            st.session_state.match_results[
                resume.name
            ] = match_result

            progress_bar.progress(
                (index + 1) / total_resumes
            )

        status_text.success(
            f"Successfully analyzed {total_resumes} resume(s)."
        )