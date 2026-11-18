import streamlit as st

from screening.ranking_engine import rank_candidates
from screening.shortlist_engine import create_shortlist
from ui.components import card, candidate_row, empty_state, nav_button, num, section_header, stat_tiles


def render():
    section_header("Shortlist", subtitle="The candidates you're moving forward with for this role.")

    match_results = st.session_state.match_results
    if not match_results:
        empty_state("No candidates screened yet", "Analyze resumes before building a shortlist.", icon="⭐")
        return

    ranked = rank_candidates(match_results)
    shortlist = create_shortlist(ranked, st.session_state.selected_candidates)

    if not shortlist:
        empty_state("Nobody shortlisted yet", "Choose Shortlist on candidates in the Ranking page.", icon="⭐")
        nav_button("Open ranking", "ranking", "sl_rank", primary=True)
        return

    average = sum(num(c["score"]) for c in shortlist) / len(shortlist)
    stat_tiles([
        ("Shortlisted", len(shortlist), f"of {len(ranked)} screened"),
        ("Average match", f"{average:.0f}%", "of the shortlist"),
        ("Best on shortlist", shortlist[0]["candidate"], f"{num(shortlist[0]['score']):.0f}% match"),
    ])

    for candidate in shortlist:
        name = candidate["candidate"]
        with card():
            col1, col2 = st.columns([5, 1.3], vertical_alignment="center")
            with col1:
                candidate_row(candidate["rank"], name, match_results[name])
            with col2:
                if st.button("Remove", key=f"shortlist_remove_{name}", width="stretch"):
                    st.session_state.selected_candidates.remove(name)
                    st.rerun()

    a, b, _ = st.columns([1, 1, 2])
    with a:
        nav_button("Compare candidates", "comparison", "sl_cmp")
    with b:
        nav_button("Export results", "export", "sl_exp", primary=True)