import streamlit as st

from ui.components import status_dot_row
from ui.state import has_candidates, has_job_profile


def render_brand():
    st.markdown(
        '<div class="ph-brand"><div class="ph-mark"><i></i><i></i><i></i></div>'
        '<div><div class="ph-brand-title">PreHier</div>'
        '<div class="ph-brand-subtitle">AI-powered hiring</div></div></div>',
        unsafe_allow_html=True,
    )


def render_status():
    st.caption("Session")
    shortlisted = len(st.session_state.get("selected_candidates", []))
    screened = len(st.session_state.get("match_results", {}))
    status_dot_row("Job profile", has_job_profile())
    status_dot_row("Candidates", has_candidates(), f"{screened} screened" if screened else None)
    status_dot_row("Shortlist", shortlisted > 0, f"{shortlisted} selected" if shortlisted else None)


def render_developer():
    st.markdown(
        '<div class="ph-sidebar-developer"><div class="ph-sidebar-developer-name">Built by Suyog Verma</div>'
        '<div class="ph-sidebar-developer-quote">"Turning ideas into working solutions"</div></div>',
        unsafe_allow_html=True,
    )