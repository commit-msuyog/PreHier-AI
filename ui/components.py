"""Reusable PreHier UI components (design-system layer).

Public API from the previous version is preserved (section_header, chip_row,
render_badge, score_row, empty_state, card, card_start/card_end, rank_pill,
candidate_header, status_dot_row) so pages keep working.
"""

import html
from contextlib import contextmanager

import streamlit as st


def _esc(value) -> str:
    return html.escape(str(value))


def _md(markup: str):
    """Render HTML via st.markdown; flattened so Markdown can't break the block."""
    flat = " ".join(line.strip() for line in markup.splitlines() if line.strip())
    st.markdown(flat, unsafe_allow_html=True)


# ---------- Navigation ----------

def go(url_path: str):
    pages = st.session_state.get("_pages") or {}
    if url_path in pages:
        st.switch_page(pages[url_path])


def nav_button(label, url_path, key, primary=False):
    if st.button(label, key=key, type="primary" if primary else "secondary", width="stretch"):
        go(url_path)


# ---------- Headers ----------

def section_header(title, subtitle=None, eyebrow=None):
    eyebrow_html = f'<div class="ph-eyebrow">{_esc(eyebrow)}</div>' if eyebrow else ""
    subtitle_html = f'<div class="ph-subtitle">{_esc(subtitle)}</div>' if subtitle else ""
    _md(f'<div class="ph-section-header">{eyebrow_html}<div class="ph-title">{_esc(title)}</div>{subtitle_html}</div>')


def subheading(text):
    _md(f'<div class="ph-h">{_esc(text)}</div>')


# ---------- Chips & badges ----------

_CHIP_VARIANTS = {"accent", "success", "warning", "danger", "muted"}


def chip_row(items, variant="muted"):
    if not items:
        return
    variant = variant if variant in _CHIP_VARIANTS else "muted"
    chips = "".join(f'<span class="ph-chip ph-chip-{variant}">{_esc(i)}</span>' for i in items)
    _md(f'<div class="ph-chip-row">{chips}</div>')


def evidence_badge(level):
    level = (level or "none").strip().lower()
    mapping = {"strong": ("ph-badge-strong", "Strong"), "partial": ("ph-badge-partial", "Partial"), "none": ("ph-badge-none", "None")}
    return mapping.get(level, ("ph-badge-neutral", level.capitalize() or "Unknown"))


def badge_html(level) -> str:
    css, label = evidence_badge(level)
    return f'<span class="ph-badge {css}">{_esc(label)}</span>'


def render_badge(level):
    _md(badge_html(level))


def rank_pill_html(rank, gold=False) -> str:
    return f'<span class="ph-rank-pill{" gold" if gold else ""}">#{_esc(rank)}</span>'


def rank_pill(rank, gold=False):
    _md(rank_pill_html(rank, gold))


# ---------- Score language ----------

def num(value, default=0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def band(value) -> str:
    v = num(value)
    return "b-high" if v >= 70 else "b-mid" if v >= 45 else "b-low"


def fit_label(value) -> str:
    return {"b-high": "Strong fit", "b-mid": "Possible fit", "b-low": "Weak fit"}[band(value)]


def fit_html(value) -> str:
    return f'<span class="ph-fit {band(value)}">{fit_label(value)}</span>'


def result_dims(result):
    """Five scoring dimensions of one match result, as (label, score)."""
    return [
        ("Required", (result.get("required_skills") or {}).get("score", 0)),
        ("Preferred", (result.get("preferred_skills") or {}).get("score", 0)),
        ("Experience", result.get("experience_score", 0)),
        ("Education", result.get("education_score", 0)),
        ("Projects", result.get("project_relevance_score", 0)),
    ]


def ring_html(value, size=64) -> str:
    v = max(0, min(num(value), 100))
    return f'<div class="ph-ring {band(v)}" style="--v:{v:.0f};--s:{size}px"><span>{v:.0f}</span></div>'


def strip_html(dims) -> str:
    segs = "".join(
        f'<div class="ph-seg"><div class="ph-seg-bar"><i class="{band(v)}" style="width:{max(0, min(num(v), 100)):.0f}%"></i></div>{_esc(l)}<b>{num(v):.0f}%</b></div>'
        for l, v in dims
    )
    return f'<div class="ph-strip">{segs}</div>'


def candidate_row(rank, name, result, ring=True):
    """Rank, name, fit label, overall ring and the five-dimension strip."""
    score = result.get("overall_score", 0)
    ring_part = ring_html(score, 60) if ring else ""
    pill = rank_pill_html(rank, gold=(rank == 1)) if rank is not None else ""
    _md(
        f'<div class="ph-cand">{ring_part}<div><div style="display:flex;align-items:center">{pill}'
        f'<span class="ph-cand-name">{_esc(name)}</span></div>{fit_html(score)}</div></div>'
        f'{strip_html(result_dims(result))}'
    )


def candidate_header(rank, name, level=None, meta=None, gold=False):
    badge = badge_html(level) if level else ""
    meta_html = f'<div class="ph-card-meta">{_esc(meta)}</div>' if meta else ""
    pill = rank_pill_html(rank, gold) if rank is not None else ""
    _md(f'<div class="ph-cand">{pill}<span class="ph-cand-name">{_esc(name)}</span>{badge}</div>{meta_html}')


def score_row(label, value):
    number = num(value, None)
    display = f"{number:.0f}%" if number is not None else "—"
    pct = 0 if number is None else max(0, min(number, 100))
    _md(f'<div class="ph-bar-row"><span>{_esc(label)}</span><div class="ph-bar"><i class="{band(pct)}" style="width:{pct:.0f}%"></i></div><b>{display}</b></div>')


def bar_row(label, value, total, color=None):
    pct = 0 if not total else max(0, min(100 * value / total, 100))
    style = f"--c:{color};" if color else ""
    _md(f'<div class="ph-bar-row"><span>{_esc(label)}</span><div class="ph-bar"><i style="{style}width:{pct:.0f}%"></i></div><b>{value}</b></div>')


def stat_tiles(tiles):
    """tiles: list of (label, value, note)."""
    html_tiles = "".join(
        f'<div class="ph-tile"><div class="ph-tile-label">{_esc(l)}</div><div class="ph-tile-value">{_esc(v)}</div><div class="ph-tile-note">{_esc(n)}</div></div>'
        for l, v, n in tiles
    )
    _md(f'<div class="ph-grid">{html_tiles}</div>')


# ---------- Empty state ----------

def empty_state(title, message, icon="📋"):
    _md(f'<div class="ph-empty"><div style="font-size:1.8rem;margin-bottom:.4rem">{_esc(icon)}</div><div class="ph-empty-title">{_esc(title)}</div><div>{_esc(message)}</div></div>')


# ---------- Cards ----------

def _card_header(title, meta):
    if title:
        st.markdown(f'<div class="ph-card-title">{_esc(title)}</div>', unsafe_allow_html=True)
    if meta:
        st.markdown(f'<div class="ph-card-meta">{_esc(meta)}</div>', unsafe_allow_html=True)


@contextmanager
def card(title=None, meta=None):
    with st.container(border=True):
        _card_header(title, meta)
        yield


_card_stack = []


def card_start(title=None, meta=None):
    container = st.container(border=True)
    container.__enter__()
    _card_stack.append(container)
    _card_header(title, meta)


def card_end():
    if _card_stack:
        _card_stack.pop().__exit__(None, None, None)


# ---------- Sidebar ----------

def status_dot_row(label, on: bool, text=None):
    dot = "ph-status-dot on" if on else "ph-status-dot off"
    state = text or ("Ready" if on else "Pending")
    _md(f'<div class="ph-status-row"><span><span class="{dot}"></span>{_esc(label)}</span><span>{_esc(state)}</span></div>')