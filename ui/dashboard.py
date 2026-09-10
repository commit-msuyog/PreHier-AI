import streamlit as st


def show_dashboard(
    candidate_profiles,
    match_results,
    selected_candidates
):

    if not match_results:
        return

    st.divider()

    st.header("📊 Recruiter Dashboard")

    total_candidates = len(candidate_profiles)

    shortlisted_count = len(
        selected_candidates
    )

    scores = [
        result.get("overall_score", 0)
        for result in match_results.values()
    ]

    average_score = (
        sum(scores) / len(scores)
        if scores
        else 0
    )

    top_candidate = max(
        match_results.items(),
        key=lambda item: item[1].get(
            "overall_score",
            0
        )
    )

    top_candidate_name = top_candidate[0]
    top_candidate_score = top_candidate[1].get(
        "overall_score",
        0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Resumes",
            total_candidates
        )

    with col2:
        st.metric(
            "Shortlisted",
            shortlisted_count
        )

    with col3:
        st.metric(
            "Average Match",
            f"{average_score:.2f}%"
        )

    with col4:
        st.metric(
            "Top Candidate",
            f"{top_candidate_score}%"
        )

    st.write(
        f"🏆 **Top Candidate:** "
        f"{top_candidate_name}"
    )