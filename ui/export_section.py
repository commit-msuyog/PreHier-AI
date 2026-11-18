import pandas as pd
import streamlit as st

from screening.comparison_engine import compare_candidates
from screening.ranking_engine import rank_candidates
from ui.components import empty_state, section_header, stat_tiles

SCORES = ["Overall Score", "Required Skills Score", "Preferred Skills Score", "Experience Score", "Education Score", "Project Relevance Score"]


def render():
    section_header("Export", subtitle="Download screening results as a CSV file for your ATS or a hiring review.")

    match_results = st.session_state.match_results
    if not match_results:
        empty_state("Nothing to export yet", "Analyze resumes on the Candidates page first.", icon="📥")
        return

    ranked = rank_candidates(match_results)
    comparison = compare_candidates(ranked, match_results)
    rank_by = {c["candidate"]: c["rank"] for c in ranked}
    shortlisted = set(st.session_state.selected_candidates)

    rows = [
        {
            "Rank": rank_by.get(e["candidate"], ""),
            "Candidate": e["candidate"],
            "Overall Score": e["overall_score"],
            "Required Skills Score": e["required_skills"],
            "Preferred Skills Score": e["preferred_skills"],
            "Experience Score": e["experience"],
            "Education Score": e["education"],
            "Project Relevance Score": e["project_relevance"],
            "Shortlisted": "Yes" if e["candidate"] in shortlisted else "No",
        }
        for e in comparison
    ]
    full = pd.DataFrame(rows).sort_values("Rank")

    stat_tiles([
        ("Candidates", len(full), "in this report"),
        ("Shortlisted", len(shortlisted & set(full["Candidate"])), "marked Yes"),
        ("Top score", f"{full['Overall Score'].max():.0f}%", full.iloc[0]["Candidate"]),
    ])

    scope = st.radio("Include", ["All candidates", "Shortlisted only"], horizontal=True)
    frame = full if scope == "All candidates" else full[full["Shortlisted"] == "Yes"]

    if frame.empty:
        st.info("No candidates are shortlisted yet. Shortlist candidates on the Ranking page, or export all candidates.")
        return

    config = {c: st.column_config.ProgressColumn(c, format="%.0f%%", min_value=0, max_value=100) for c in SCORES}
    st.dataframe(frame, column_config=config, width="stretch", hide_index=True)

    st.download_button(
        label=f"Download CSV ({len(frame)} candidates)",
        data=frame.to_csv(index=False).encode("utf-8"),
        file_name="prehier_screening_results.csv" if scope == "All candidates" else "prehier_shortlist.csv",
        mime="text/csv",
        type="primary",
    )