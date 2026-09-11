import pandas as pd
import streamlit as st

from screening.comparison_engine import compare_candidates
from screening.ranking_engine import rank_candidates
from ui.components import empty_state, section_header


def render():
    section_header(
        "Export",
        subtitle="Download the full screening results as a CSV file.",
    )

    match_results = st.session_state.match_results

    if not match_results:
        empty_state(
            "Nothing to export yet",
            "Analyze resumes on the Candidates page before exporting results.",
            icon="📥",
        )
        return

    ranked_candidates = rank_candidates(match_results)
    comparison = compare_candidates(ranked_candidates, match_results)

    rank_by_candidate = {c["candidate"]: c["rank"] for c in ranked_candidates}
    shortlisted = set(st.session_state.selected_candidates)

    rows = []
    for entry in comparison:
        rows.append(
            {
                "Rank": rank_by_candidate.get(entry["candidate"], ""),
                "Candidate": entry["candidate"],
                "Overall Score": entry["overall_score"],
                "Required Skills Score": entry["required_skills"],
                "Preferred Skills Score": entry["preferred_skills"],
                "Experience Score": entry["experience"],
                "Education Score": entry["education"],
                "Project Relevance Score": entry["project_relevance"],
                "Shortlisted": "Yes" if entry["candidate"] in shortlisted else "No",
            }
        )

    dataframe = pd.DataFrame(rows).sort_values("Rank")

    st.dataframe(dataframe, width="stretch", hide_index=True)

    csv_data = dataframe.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Screening Results (CSV)",
        data=csv_data,
        file_name="prehier_screening_results.csv",
        mime="text/csv",
        type="primary",
    )
