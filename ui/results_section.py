import streamlit as st

from ui.components import chip_row, empty_state, render_badge, score_row, section_header



def _render_skills_block(title, skill_result, preferred=False):
    st.markdown(f"**{title}**")

    exact = skill_result.get(
        "exact_matches",
        skill_result.get("matched_skills", skill_result.get("matched", []))
    )

    related = skill_result.get("related_matches", [])
    semantic = skill_result.get("semantic_matches", [])

    missing = skill_result.get(
        "missing_skills",
        skill_result.get("missing", [])
    )

    if exact:
        st.caption("Exact Matches")
        chip_row(exact, variant="success")

    if related:
        st.caption("Related Technology Matches")
        for match in related:
            st.write(
                f"• **{match['required_skill']}** "
                f"← {match['matched_skill']} "
                f"({match['credit'] * 100:.0f}% credit)"
            )

    if semantic:
        st.caption("Semantic Matches")
        for match in semantic:
            st.write(
                f"• **{match['required_skill']}** "
                f"← {match['matched_skill']} "
                f"(similarity: {match['similarity']})"
            )

    if missing:
        st.caption("Missing Skills")
        chip_row(missing, variant="danger")

    if not exact and not related and not semantic:
        st.caption("No matching skills found.")

    if not missing:
        st.caption("No missing skills.")



def _render_evidence(evidence_result):
    st.markdown("#### Requirement Evidence")

    requirements = evidence_result.get("requirements") if isinstance(evidence_result, dict) else None

    if not requirements:
        st.caption("No requirement evidence available for this candidate.")
        return

    for requirement in requirements:
        skill = requirement.get("skill", "")
        level = requirement.get("evidence_level", "none")
        evidence = requirement.get("evidence", "")

        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{skill}**")
        with col2:
            render_badge(level)
        if evidence:
            st.caption(evidence)
        st.markdown("<div style='margin-bottom:0.4rem'></div>", unsafe_allow_html=True)


def _render_projects(project_result):
    st.markdown("#### Project Relevance")

    projects = project_result.get("projects") if isinstance(project_result, dict) else None

    if not projects:
        st.caption("No project relevance information available for this candidate.")
        return

    overall = project_result.get("overall_relevance", "none")
    st.write("Overall relevance:")
    render_badge(overall)

    for project in projects:
        title = project.get("title", "Unnamed Project")
        relevance = project.get("relevance", "none")
        reason = project.get("reason", "")

        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{title}**")
        with col2:
            render_badge(relevance)
        if reason:
            st.caption(reason)
        st.markdown("<div style='margin-bottom:0.4rem'></div>", unsafe_allow_html=True)


def _render_candidate_result(name, result):
    st.markdown(f"### {name}")

    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("Overall Match", f"{result.get('overall_score', 0)}%")

    with col2:
        score_row("Required Skills", result.get("required_skills", {}).get("score", 0))
        score_row("Preferred Skills", result.get("preferred_skills", {}).get("score", 0))
        score_row("Experience", result.get("experience_score", 0))
        score_row("Education", result.get("education_score", 0))
        score_row("Project Relevance", result.get("project_relevance_score", 0))

    with st.expander("View full skill match, evidence & project relevance"):
        required = result.get("required_skills", {})
        _render_skills_block(
            "Required Skills",
            required,
        )

        preferred = result.get("preferred_skills", {})
        _render_skills_block(
            "Preferred Skills",
            preferred,
            preferred=True,
        )

        st.divider()
        _render_evidence(result.get("evidence", {}))

        st.divider()
        _render_projects(result.get("projects", {}))

    st.divider()


def render():
    section_header(
        "Screening Results",
        subtitle="Detailed, explainable scoring for every candidate screened against the job profile.",
    )

    match_results = st.session_state.match_results

    if not match_results:
        empty_state(
            "No screening results yet",
            "Analyze candidates on the Candidates page to see detailed "
            "scoring here.",
            icon="📊",
        )
        return

    # Show strongest matches first.
    ordered = sorted(
        match_results.items(),
        key=lambda item: item[1].get("overall_score", 0),
        reverse=True,
    )

    for name, result in ordered:
        _render_candidate_result(name, result)
