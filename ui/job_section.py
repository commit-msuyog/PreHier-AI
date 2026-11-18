import streamlit as st

from ai.job_analyzer import analyze_job_description
from ui.components import chip_row, empty_state, section_header, stat_tiles, subheading


def _render_job_profile(job_profile):
    subheading(job_profile.get("job_title") or "Untitled role")

    experience = job_profile.get("experience_required", {}) or {}
    years = experience.get("years", 0)
    education = job_profile.get("education", [])
    required = job_profile.get("required_skills", [])
    preferred = job_profile.get("preferred_skills", [])

    stat_tiles([
        ("Experience", f"{years}+ yrs" if years and years > 0 else "Open", experience.get("description", "") or "Not specified"),
        ("Must-have skills", len(required), "weighted most in scoring"),
        ("Nice-to-have skills", len(preferred), "extra credit"),
    ])

    with st.container(border=True):
        st.markdown("**Must-have skills**")
        chip_row(required, "accent") if required else st.caption("No required skills found. Try adding explicit requirements to the description.")
        st.markdown("**Nice-to-have skills**")
        chip_row(preferred, "muted") if preferred else st.caption("No preferred skills found.")
        st.markdown("**Education**")
        chip_row(education, "muted") if education else st.caption("Not specified.")

    responsibilities = job_profile.get("responsibilities", [])
    if responsibilities:
        with st.expander("Responsibilities"):
            for item in responsibilities:
                st.markdown(f"- {item}")

    with st.expander("Developer details (raw JSON)"):
        st.json(job_profile)


def render():
    section_header(
        "Job setup",
        subtitle="Paste the job description. PreHier extracts the requirements every candidate is screened against.",
    )

    job_description = st.text_area(
        "Job description",
        value=st.session_state.job_description_text,
        placeholder="Paste the full job description here, including requirements and responsibilities.",
        height=240,
        label_visibility="collapsed",
    )
    st.session_state.job_description_text = job_description
    words = len(job_description.split())
    st.caption(f"{words} words" if words else "Longer, more specific descriptions give better skill extraction.")

    analyze_clicked = st.button("Analyze job description", type="primary", disabled=not job_description.strip())

    if analyze_clicked:
        with st.spinner("Reading the job description..."):
            job_profile = analyze_job_description(job_description)

        if job_profile and "error" in job_profile:
            st.error("The job description could not be analyzed. Try again, or shorten and simplify the text.")
            with st.expander("Developer details"):
                st.write(job_profile.get("error"))
                if "raw_response" in job_profile:
                    st.code(job_profile["raw_response"])
        else:
            st.session_state.job_profile = job_profile
            st.success("Job analyzed. Upload resumes on the Candidates page to start screening.")

    st.divider()

    if st.session_state.job_profile and "error" not in st.session_state.job_profile:
        _render_job_profile(st.session_state.job_profile)
    else:
        empty_state(
            "No job profile yet",
            "After analysis you'll see the experience level, must-have skills and nice-to-have skills here.",
            icon="💼",
        )