import streamlit as st

from screening.ranking_engine import rank_candidates
from screening.comparison_engine import compare_candidates


def show_comparison(match_results):

    st.divider()

    st.header("📊 Candidate Comparison")

    if not match_results:
        st.info(
            "Analyze resumes to compare candidates."
        )
        return

    ranked_candidates = rank_candidates(
        match_results
    )

    comparison = compare_candidates(
        ranked_candidates,
        match_results
    )

    st.dataframe(
        comparison,
        use_container_width=True
    )
    