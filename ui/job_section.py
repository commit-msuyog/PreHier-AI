import streamlit as st

from ai.job_analyzer import analyze_job_description


def show_job_section():

    st.divider()

    st.header("💼 Job Description")

    job_description = st.text_area(
        "Paste the job description here",
        placeholder="Paste the job description of the role you are hiring for...",
        height=250
    )

    if job_description:
        if st.button("Analyze Job Description"):
            with st.spinner("Analyzing job description..."):
                job_profile = analyze_job_description(
                    job_description
                )

                st.session_state.job_profile = job_profile

    if st.session_state.job_profile:
        st.subheader("💼 Job Profile")
        st.json(st.session_state.job_profile)

    return st.session_state.job_profile