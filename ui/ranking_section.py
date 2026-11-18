import streamlit as st

from screening.ranking_engine import rank_candidates
from ui.components import card, candidate_row, empty_state, num, section_header


def render():
    section_header("Ranking", subtitle="Candidates ordered by overall match. Shortlist straight from here.")

    match_results = st.session_state.match_results
    if not match_results:
        empty_state("No ranking yet", "Analyze resumes on the Candidates page to rank candidates.", icon="🏆")
        return

    ranked = rank_candidates(match_results)

    f1, f2, f3 = st.columns([2, 2, 1.4], vertical_alignment="bottom")
    query = f1.text_input("Search", placeholder="Filter by name").strip().lower()
    minimum = f2.slider("Minimum match", 0, 100, 0, format="%d%%")
    only_short = f3.toggle("Shortlisted only")

    visible = [
        c for c in ranked
        if query in c["candidate"].lower()
        and num(c["score"]) >= minimum
        and (not only_short or c["candidate"] in st.session_state.selected_candidates)
    ]
    st.caption(f"Showing {len(visible)} of {len(ranked)} candidates")

    if not visible:
        empty_state("No candidates match these filters", "Lower the minimum match or clear the search.", icon="🔍")
        return

    for candidate in visible:
        name = candidate["candidate"]
        is_short = name in st.session_state.selected_candidates
        with card():
            col1, col2 = st.columns([5, 1.3], vertical_alignment="center")
            with col1:
                candidate_row(candidate["rank"], name, match_results[name])
            with col2:
                if is_short:
                    st.success("Shortlisted")
                    if st.button("Remove", key=f"remove_{name}", width="stretch"):
                        st.session_state.selected_candidates.remove(name)
                        st.rerun()
                elif st.button("Shortlist", key=f"shortlist_{name}", type="primary", width="stretch"):
                    st.session_state.selected_candidates.append(name)
                    st.rerun()