import streamlit as st

from ai.job_analyzer import analyze_job_description
from ui.components import chip_row, empty_state, section_header


def _render_job_profile(job_profile):
    st.markdown(f"### {job_profile.get('job_title') or 'Untitled Role'}")

    experience = job_profile.get("experience_required", {}) or {}
    years = experience.get("years", 0)
    exp_description = experience.get("description", "")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Experience Required**")
        if years and years > 0:
            st.write(f"{years}+ years")
        else:
            st.write("Not specified")
        if exp_description:
            st.caption(exp_description)

    with col2:
        st.markdown("**Education**")
        education = job_profile.get("education", [])
        if education:
            chip_row(education, variant="muted")
        else:
            st.write("Not specified")

    st.markdown("**Required Skills**")
    required_skills = job_profile.get("required_skills", [])
    if required_skills:
        chip_row(required_skills, variant="accent")
    else:
        st.caption("No required skills extracted.")

    st.markdown("**Preferred Skills**")
    preferred_skills = job_profile.get("preferred_skills", [])
    if preferred_skills:
        chip_row(preferred_skills, variant="muted")
    else:
        st.caption("No preferred skills extracted.")

    responsibilities = job_profile.get("responsibilities", [])
    if responsibilities:
        st.markdown("**Responsibilities**")
        for item in responsibilities:
            st.markdown(f"- {item}")

    with st.expander("Developer details (raw JSON)"):
        st.json(job_profile)


def render():
    section_header(
        "Job Setup",
        subtitle="Paste the job description to extract the requirements PreHier will screen candidates against.",
    )

    job_description = st.text_area(
        "Job description",
        value=st.session_state.job_description_text,
        placeholder="Paste the job description of the role you are hiring for...",
        height=240,
        label_visibility="collapsed",
    )
    st.session_state.job_description_text = job_description

    analyze_clicked = st.button(
        "Analyze Job Description",
        type="primary",
        disabled=not job_description.strip(),
    )

    if analyze_clicked:
        with st.spinner("Analyzing job description with AI..."):
            job_profile = analyze_job_description(job_description)

        if job_profile and "error" in job_profile:
            st.error(
                "Unable to analyze this job description. Please try again "
                "or simplify the text."
            )
            with st.expander("Developer details"):
                st.write(job_profile.get("error"))
                if "raw_response" in job_profile:
                    st.code(job_profile["raw_response"])
        else:
            st.session_state.job_profile = job_profile
            st.success("Job description analyzed successfully.")

    st.divider()

    if st.session_state.job_profile and "error" not in st.session_state.job_profile:
        _render_job_profile(st.session_state.job_profile)
    else:
        empty_state(
            "No job profile yet",
            "Paste a job description above and click \"Analyze Job Description\" "
            "to extract the requirements PreHier will screen candidates against.",
            icon="💼",
        )
