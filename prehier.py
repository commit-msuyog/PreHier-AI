import streamlit as st

from ui.job_section import show_job_section
from ui.resume_section import show_resume_section
from ui.results_section import show_results
from ui.ranking_section import show_ranking
from ui.shortlist_section import show_shortlist
from ui.comparison_section import show_comparison
from ui.dashboard import show_dashboard


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

if "selected_candidates" not in st.session_state:
    st.session_state.selected_candidates = []


st.title("🎯 PreHier")
st.subheader("AI-Powered Pre-Hire Screening")

st.write(
    "Screen and shortlist candidates based on your job requirements."
)


job_profile = show_job_section()

show_resume_section(
    job_profile
)

show_results(
    st.session_state.candidate_profiles,
    st.session_state.match_results
)

show_dashboard(
    st.session_state.candidate_profiles,
    st.session_state.match_results,
    st.session_state.selected_candidates
)

show_ranking(
    st.session_state.match_results
)

show_shortlist(
    st.session_state.match_results
)

show_comparison(
    st.session_state.match_results
)