import streamlit as st

from screening.ranking_engine import rank_candidates
from screening.shortlist_engine import create_shortlist
from ui.components import card_end, card_start, empty_state, rank_pill, section_header


def render():
    section_header(
        "Shortlist",
        subtitle="Candidates you've marked as shortlisted for this role.",
    )

    match_results = st.session_state.match_results

    if not match_results:
        empty_state(
            "No candidates screened yet",
            "Analyze resumes before building a shortlist.",
            icon="⭐",
        )
        return

    ranked_candidates = rank_candidates(match_results)
    shortlist = create_shortlist(ranked_candidates, st.session_state.selected_candidates)

    if not shortlist:
        empty_state(
            "No candidates shortlisted yet",
            "Go to the Ranking page and click \"Shortlist\" on the "
            "candidates you'd like to move forward with.",
            icon="⭐",
        )
        return

    for candidate in shortlist:
        card_start()
        col1, col2 = st.columns([4, 1])
        with col1:
            rank_pill(candidate["rank"], gold=(candidate["rank"] == 1))
            st.markdown(f"**{candidate['candidate']}**")
            st.caption(f"Overall Match Score: {candidate['score']}%")
        with col2:
            if st.button("Remove", key=f"shortlist_remove_{candidate['candidate']}", width="stretch"):
                st.session_state.selected_candidates.remove(candidate["candidate"])
                st.rerun()
        card_end()
