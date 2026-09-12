import streamlit as st

from ui.components import status_dot_row
from ui.state import has_candidates, has_job_profile


def render_brand():
    st.markdown(
        """
        <div class="ph-brand">
            <div class="ph-brand-text">
                <div class="ph-brand-title">PreHier</div>
                <div class="ph-brand-subtitle">Pre-Hire Screening</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status():
    st.caption("SESSION STATUS")

    col1, col2 = st.columns(2)

    with col1:
        st.toggle(
            "Job",
            value=has_job_profile(),
            disabled=True,
        )

    with col2:
        st.toggle(
            "Candidates",
            value=has_candidates(),
            disabled=True,
        )
def render_developer():
    st.markdown(
        """
        <div class="ph-sidebar-developer">
            <div class="ph-sidebar-developer-name">
                Built by Suyog Verma
            </div>
            <div class="ph-sidebar-developer-quote">
                "Turning ideas into working solutions"
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

