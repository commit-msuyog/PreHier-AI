import pandas as pd
import streamlit as st

from ui.components import chip_row, empty_state, section_header
from ui.state import has_candidates, has_job_profile


def _render_getting_started():
    st.markdown("Get started in two steps:")
    st.markdown(
        "1. **Job Setup** — paste the job description and analyze it.\n"
        "2. **Candidates** — upload resumes and run AI screening."
    )
    empty_state(
        "No screening data yet",
        "Once you analyze a job description and screen candidates, this "
        "dashboard will summarize the results.",
        icon="🎯",
    )


def render():
    section_header(
        "Dashboard",
        subtitle="A snapshot of the current screening session.",
    )

    match_results = st.session_state.match_results
    candidate_profiles = st.session_state.candidate_profiles
    selected_candidates = st.session_state.selected_candidates

    if not has_job_profile() and not has_candidates():
        _render_getting_started()
        return

    if has_job_profile() and not has_candidates():
        job_profile = st.session_state.job_profile
        st.markdown(f"**Job profile ready:** {job_profile.get('job_title') or 'Untitled role'}")
        required_skills = job_profile.get("required_skills", [])
        if required_skills:
            chip_row(required_skills, variant="accent")
        st.info("Head to the Candidates page to upload and screen resumes.")
        return

    total_candidates = len(candidate_profiles)
    shortlisted_count = len(selected_candidates)

    scores = [result.get("overall_score", 0) for result in match_results.values()]
    average_score = sum(scores) / len(scores) if scores else 0

    top_candidate_name, top_candidate_result = max(
        match_results.items(),
        key=lambda item: item[1].get("overall_score", 0),
    )
    top_candidate_score = top_candidate_result.get("overall_score", 0)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Candidates", total_candidates)
    col2.metric("Average Match Score", f"{average_score:.1f}%")
    col3.metric("Shortlisted", shortlisted_count)
    col4.metric("Top Candidate", f"{top_candidate_score}%", help=top_candidate_name)

    st.markdown(f"**Top candidate:** {top_candidate_name}")

    st.divider()
    st.markdown("#### Candidate Match Distribution")

    chart_data = pd.DataFrame(
        {
            "Candidate": list(match_results.keys()),
            "Overall Match (%)": [result.get("overall_score", 0) for result in match_results.values()],
        }
    ).sort_values("Overall Match (%)", ascending=False).set_index("Candidate")

    st.bar_chart(chart_data, height=280)
