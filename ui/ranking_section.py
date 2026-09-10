import streamlit as st

from screening.ranking_engine import rank_candidates


def show_ranking(match_results):

    st.divider()

    st.header("🏆 Candidate Ranking")

    if not match_results:
        st.info(
            "Analyze resumes to generate the candidate ranking."
        )
        return

    ranked_candidates = rank_candidates(
        match_results
    )

    for candidate in ranked_candidates:

        candidate_name = candidate["candidate"]
        score = candidate["score"]

        st.write(
            f"**#{candidate['rank']} — "
            f"{candidate_name}**"
        )

        st.progress(
            min(score / 100, 1.0)
        )

        st.caption(
            f"Overall Match Score: {score}%"
        )

        if candidate_name in st.session_state.selected_candidates:
            st.success("⭐ Shortlisted")

        else:
            if st.button(
                "⭐ Shortlist",
                key=f"shortlist_{candidate_name}"
            ):
                st.session_state.selected_candidates.append(
                    candidate_name
                )

                st.rerun()