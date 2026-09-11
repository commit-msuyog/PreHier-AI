"""Sidebar branding and at-a-glance session status shown on every page."""

import streamlit as st

from ui.components import status_dot_row
from ui.state import has_candidates, has_job_profile


def render_brand():
    st.markdown(
        """
        <div class="ph-brand">
            <div class="ph-brand-mark">PH</div>
            <div class="ph-brand-text">
                <div class="ph-brand-title">PreHier</div>
                <div class="ph-brand-subtitle">Pre-Hire Screening</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status():
    match_results = st.session_state.get("match_results", {})
    shortlisted = st.session_state.get("selected_candidates", [])

    st.caption("SESSION STATUS")
    status_dot_row("Job description analyzed", has_job_profile())
    status_dot_row("Candidates screened", has_candidates())

    if match_results:
        st.markdown(
            f'<div class="ph-status-list">'
            f'<div class="ph-status-row"><span>Candidates screened</span><span>{len(match_results)}</span></div>'
            f'<div class="ph-status-row"><span>Shortlisted</span><span>{len(shortlisted)}</span></div>'
            f"</div>",
            unsafe_allow_html=True,
        )
