import streamlit as st

from screening.ranking_engine import rank_candidates
from ui.components import card_end, card_start, empty_state, rank_pill, section_header


def render():
    section_header(
        "Ranking",
        subtitle="Candidates ranked by overall match score. Shortlist directly from here.",
    )

    match_results = st.session_state.match_results

    if not match_results:
        empty_state(
            "No ranking yet",
            "Analyze resumes on the Candidates page to generate the "
            "candidate ranking.",
            icon="🏆",
        )
        return

    ranked_candidates = rank_candidates(match_results)

    for candidate in ranked_candidates:
        candidate_name = candidate["candidate"]
        score = candidate["score"]
        is_shortlisted = candidate_name in st.session_state.selected_candidates

        card_start()
        col1, col2 = st.columns([4, 1])

        with col1:
            rank_pill(candidate["rank"], gold=(candidate["rank"] == 1))
            st.markdown(f"**{candidate_name}**")
            st.progress(min(score / 100, 1.0))
            st.caption(f"Overall Match Score: {score}%")

        with col2:
            if is_shortlisted:
                st.success("Shortlisted")
                if st.button("Remove", key=f"remove_{candidate_name}", width="stretch"):
                    st.session_state.selected_candidates.remove(candidate_name)
                    st.rerun()
            else:
                if st.button("Shortlist", key=f"shortlist_{candidate_name}", type="primary", width="stretch"):
                    st.session_state.selected_candidates.append(candidate_name)
                    st.rerun()

        card_end()
