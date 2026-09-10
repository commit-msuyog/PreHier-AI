import streamlit as st

from screening.ranking_engine import rank_candidates
from screening.shortlist_engine import create_shortlist


def show_shortlist(match_results):

    st.divider()

    st.header("⭐ Shortlisted Candidates")

    if not match_results:
        st.info(
            "Analyze resumes before creating a shortlist."
        )
        return

    ranked_candidates = rank_candidates(
        match_results
    )

    shortlist = create_shortlist(
        ranked_candidates,
        st.session_state.selected_candidates
    )

    if shortlist:

        for candidate in shortlist:

            st.write(
                f"**#{candidate['rank']} — "
                f"{candidate['candidate']}**"
            )

            st.caption(
                f"Overall Match Score: "
                f"{candidate['score']}%"
            )

    else:
        st.info(
            "No candidates have been shortlisted yet."
        )
        