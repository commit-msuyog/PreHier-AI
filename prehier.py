import streamlit as st

from ui import comparison_section, dashboard, export_section, job_section
from ui import ranking_section, resume_section, results_section, shortlist_section
from ui.sidebar import render_brand, render_status, render_developer
from ui.state import init_session_state
from ui.styles import inject_css

st.set_page_config(
    page_title="PreHier",
    page_icon= "assets/prehier-logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
init_session_state()

with st.sidebar:
    render_brand()

pages = [
    st.Page(dashboard.render, title="Dashboard", icon=":material/dashboard:", url_path="dashboard", default=True),
    st.Page(job_section.render, title="Job Setup", icon=":material/work:", url_path="job-setup"),
    st.Page(resume_section.render, title="Candidates", icon=":material/group:", url_path="candidates"),
    st.Page(results_section.render, title="Screening Results", icon=":material/fact_check:", url_path="results"),
    st.Page(ranking_section.render, title="Ranking", icon=":material/leaderboard:", url_path="ranking"),
    st.Page(shortlist_section.render, title="Shortlist", icon=":material/star:", url_path="shortlist"),
    st.Page(comparison_section.render, title="Comparison", icon=":material/compare_arrows:", url_path="comparison"),
    st.Page(export_section.render, title="Export", icon=":material/download:", url_path="export"),
]
current_page = st.navigation(pages, position="sidebar")

with st.sidebar:
    st.divider()
    render_status()
    render_developer()

current_page.run()
