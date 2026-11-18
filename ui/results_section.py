import streamlit as st

from ui.components import (
    _esc, _md, badge_html, candidate_row, chip_row, empty_state, num,
    result_dims, section_header, subheading,
)


def _insights(result):
    dims = result_dims(result)
    best = max(dims, key=lambda d: num(d[1]))
    worst = min(dims, key=lambda d: num(d[1]))
    required = result.get("required_skills", {}) or {}
    missing = required.get("missing_skills", required.get("missing", [])) or []
    items = [f"Strongest area: <b>{_esc(best[0].lower())}</b> at {num(best[1]):.0f}%."]
    if num(worst[1]) < 60:
        items.append(f"Weakest area: <b>{_esc(worst[0].lower())}</b> at {num(worst[1]):.0f}%.")
    if missing:
        shown = ", ".join(_esc(m) for m in missing[:4])
        more = f" and {len(missing) - 4} more" if len(missing) > 4 else ""
        items.append(f"Missing {len(missing)} required skill(s): {shown}{more}.")
    else:
        items.append("Covers every required skill.")
    _md("<ul class='ph-insights'>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>")


def _render_skills_block(title, skill_result):
    st.markdown(f"**{title}**")
    exact = skill_result.get("exact_matches", skill_result.get("matched_skills", skill_result.get("matched", [])))
    related = skill_result.get("related_matches", [])
    semantic = skill_result.get("semantic_matches", [])
    missing = skill_result.get("missing_skills", skill_result.get("missing", []))

    if exact:
        st.caption("Exact matches")
        chip_row(exact, "success")
    if related:
        st.caption("Related technology")
        for m in related:
            st.write(f"• **{m['required_skill']}** ← {m['matched_skill']} ({m['credit'] * 100:.0f}% credit)")
    if semantic:
        st.caption("Semantic matches")
        for m in semantic:
            st.write(f"• **{m['required_skill']}** ← {m['matched_skill']} (similarity: {m['similarity']})")
    if missing:
        st.caption("Missing")
        chip_row(missing, "danger")
    if not exact and not related and not semantic:
        st.caption("No matching skills found.")
    if not missing:
        st.caption("Nothing missing.")


def _render_rows(items, title_key, level_key, text_key):
    for item in items:
        text = item.get(text_key, "")
        text_html = f"<p>{_esc(text)}</p>" if text else ""
        _md(f'<div class="ph-ev"><div><b>{_esc(item.get(title_key, ""))}</b>{text_html}</div>{badge_html(item.get(level_key, "none"))}</div>')


def _render_evidence(evidence_result):
    requirements = evidence_result.get("requirements") if isinstance(evidence_result, dict) else None
    if not requirements:
        st.caption("No requirement evidence available for this candidate.")
        return
    st.caption("What the resume shows for each requirement")
    _render_rows(requirements, "skill", "evidence_level", "evidence")


def _render_projects(project_result):
    projects = project_result.get("projects") if isinstance(project_result, dict) else None
    if not projects:
        st.caption("No project information available for this candidate.")
        return
    _md(f'<div class="ph-note">Overall relevance {badge_html(project_result.get("overall_relevance", "none"))}</div>')
    _render_rows(projects, "title", "relevance", "reason")


def render():
    section_header("Screening results", subtitle="Pick a candidate to see exactly how their score was built.")

    match_results = st.session_state.match_results
    if not match_results:
        empty_state("No results yet", "Analyze resumes on the Candidates page to see scoring here.", icon="📊")
        return

    ordered = sorted(match_results.items(), key=lambda i: num(i[1].get("overall_score", 0)), reverse=True)
    names = [n for n, _ in ordered]
    labels = {n: f"#{i} {n}  ({num(r.get('overall_score', 0)):.0f}%)" for i, (n, r) in enumerate(ordered, 1)}

    name = st.selectbox("Candidate", names, format_func=lambda n: labels[n])
    result = match_results[name]
    rank = names.index(name) + 1

    with st.container(border=True):
        candidate_row(rank, name, result)
        _insights(result)

    tab_skills, tab_evidence, tab_projects = st.tabs(["Skill match", "Requirement evidence", "Projects"])
    with tab_skills:
        _render_skills_block("Required skills", result.get("required_skills", {}))
        st.divider()
        _render_skills_block("Preferred skills", result.get("preferred_skills", {}))
    with tab_evidence:
        _render_evidence(result.get("evidence", {}))
    with tab_projects:
        _render_projects(result.get("projects", {}))