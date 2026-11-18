import streamlit as st

from screening.ranking_engine import rank_candidates
from ui.components import (
    _esc, _md, bar_row, band, candidate_row, chip_row, empty_state, fit_label,
    nav_button, num, result_dims, ring_html, section_header, stat_tiles,
    strip_html, subheading,
)
from ui.state import has_candidates, has_job_profile


def _hero(name, result):
    score = num(result.get("overall_score", 0))
    _md(
        f'<div class="ph-hero"><div class="ph-hero-top">{ring_html(score)}'
        f'<div><div class="lbl">Best match for this role</div><div class="nm">{_esc(name)}</div>'
        f'<div class="lbl">{fit_label(score)}</div></div></div>{strip_html(result_dims(result))}</div>'
    )


def _empty_start():
    empty_state(
        "Start with the job description",
        "Analyze a role first, then upload resumes. This page then shows who fits best and why.",
        icon="🎯",
    )
    c1, c2, _ = st.columns([1, 1, 2])
    with c1:
        nav_button("Set up the job", "job-setup", "dash_job", primary=True)
    with c2:
        nav_button("Upload resumes", "candidates", "dash_cand")


def render():
    section_header("Dashboard", subtitle="Where the current screening stands and who to look at first.")

    match_results = st.session_state.match_results
    selected = st.session_state.selected_candidates

    if not has_job_profile() and not has_candidates():
        _empty_start()
        return

    if not has_candidates():
        profile = st.session_state.job_profile
        subheading(profile.get("job_title") or "Untitled role")
        st.caption("Job profile ready. Required skills:")
        chip_row(profile.get("required_skills", []), variant="accent")
        nav_button("Upload and screen resumes", "candidates", "dash_upload", primary=True)
        return

    ranked = rank_candidates(match_results)
    total = len(ranked)
    scores = [num(r.get("overall_score", 0)) for r in match_results.values()]
    average = sum(scores) / total if total else 0
    strong = sum(1 for s in scores if band(s) == "b-high")
    mid = sum(1 for s in scores if band(s) == "b-mid")
    weak = total - strong - mid
    top = ranked[0]

    left, right = st.columns([3, 2], gap="medium")
    with left:
        _hero(top["candidate"], match_results[top["candidate"]])
    with right:
        stat_tiles([
            ("Candidates screened", total, "in this session"),
            ("Average match", f"{average:.0f}%", "across all candidates"),
            ("Strong fits", strong, "scoring 70% or more"),
            ("Shortlisted", len(selected), f"of {total}"),
        ])

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        with st.container(border=True):
            subheading("Hiring funnel")
            bar_row("Screened", total, total)
            bar_row("Strong fit", strong, total, "var(--ph-good)")
            bar_row("Shortlisted", len(selected), total, "var(--ph-amber)")
    with c2:
        with st.container(border=True):
            subheading("Score bands")
            bar_row("70% and above", strong, total, "var(--ph-good)")
            bar_row("45% to 69%", mid, total, "var(--ph-amber)")
            bar_row("Below 45%", weak, total, "var(--ph-bad)")

    subheading("Top candidates")
    for cand in ranked[:5]:
        with st.container(border=True):
            candidate_row(cand["rank"], cand["candidate"], match_results[cand["candidate"]])

    st.write("")
    a, b, c, _ = st.columns([1, 1, 1, 2])
    with a:
        nav_button("See all results", "results", "dash_results")
    with b:
        nav_button("Open ranking", "ranking", "dash_rank")
    with c:
        nav_button("Compare candidates", "comparison", "dash_cmp")