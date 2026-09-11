import pandas as pd
import streamlit as st

from screening.comparison_engine import compare_candidates
from screening.ranking_engine import rank_candidates
from ui.components import empty_state, section_header


def render():
    section_header(
        "Comparison",
        subtitle="Compare candidates side by side across every scoring dimension.",
    )

    match_results = st.session_state.match_results

    if not match_results:
        empty_state(
            "Nothing to compare yet",
            "Analyze resumes on the Candidates page to compare candidates here.",
            icon="📊",
        )
        return

    ranked_candidates = rank_candidates(match_results)
    comparison = compare_candidates(ranked_candidates, match_results)

    dataframe = pd.DataFrame(comparison).rename(
        columns={
            "candidate": "Candidate",
            "overall_score": "Overall",
            "required_skills": "Required Skills",
            "preferred_skills": "Preferred Skills",
            "experience": "Experience",
            "education": "Education",
            "project_relevance": "Project Relevance",
        }
    )

    score_columns = [
        "Overall",
        "Required Skills",
        "Preferred Skills",
        "Experience",
        "Education",
        "Project Relevance",
    ]

    column_config = {
        column: st.column_config.ProgressColumn(
            column,
            format="%.0f%%",
            min_value=0,
            max_value=100,
        )
        for column in score_columns
    }

    st.dataframe(
        dataframe,
        column_config=column_config,
        width="stretch",
        hide_index=True,
    )
