import pandas as pd
import streamlit as st

from screening.comparison_engine import compare_candidates
from screening.ranking_engine import rank_candidates
from ui.components import _esc, _md, band, empty_state, fit_html, num, section_header

DIMENSIONS = [
    ("overall_score", "Overall"), ("required_skills", "Required skills"), ("preferred_skills", "Preferred skills"),
    ("experience", "Experience"), ("education", "Education"), ("project_relevance", "Project relevance"),
]


def _table(rows):
    head = "".join(f"<th>{_esc(r['candidate'])}</th>" for r in rows)
    body = ""
    for key, label in DIMENSIONS:
        top = max(num(r[key]) for r in rows)
        cells = ""
        for r in rows:
            v = num(r[key])
            best = "best" if len(rows) > 1 and v == top and top > 0 else ""
            cells += (f'<td class="{best}"><span class="v">{v:.0f}%</span><div class="ph-bar" style="margin-top:.3rem">'
                      f'<i class="{band(v)}" style="width:{max(0, min(v, 100)):.0f}%"></i></div></td>')
        body += f'<tr><td class="dim">{label}</td>{cells}</tr>'
    fits = "".join(f"<td>{fit_html(r['overall_score'])}</td>" for r in rows)
    body += f'<tr><td class="dim">Verdict</td>{fits}</tr>'
    _md(f'<div class="ph-table-wrap"><table class="ph-table"><thead><tr><th></th>{head}</tr></thead><tbody>{body}</tbody></table></div>')


def render():
    section_header("Comparison", subtitle="Put up to four candidates side by side. The best score in each row is marked.")

    match_results = st.session_state.match_results
    if not match_results:
        empty_state("Nothing to compare yet", "Analyze resumes on the Candidates page first.", icon="📊")
        return

    ranked = rank_candidates(match_results)
    comparison = compare_candidates(ranked, match_results)
    by_name = {c["candidate"]: c for c in comparison}
    order = [c["candidate"] for c in ranked if c["candidate"] in by_name]

    chosen = st.multiselect("Candidates to compare", order, default=order[:3], max_selections=4)
    if len(chosen) < 2:
        st.info("Choose at least two candidates to compare.")
    else:
        _table([by_name[n] for n in order if n in chosen])

    with st.expander("All candidates (table)"):
        df = pd.DataFrame(comparison).rename(columns={k: l for k, l in DIMENSIONS} | {"candidate": "Candidate"})
        cols = {l: st.column_config.ProgressColumn(l, format="%.0f%%", min_value=0, max_value=100) for _, l in DIMENSIONS}
        st.dataframe(df, column_config=cols, width="stretch", hide_index=True)