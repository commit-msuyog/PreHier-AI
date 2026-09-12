"""
Small reusable Streamlit UI components shared across PreHier pages.

Keeping these in one place is what lets every page share the same
premium visual language without duplicating HTML snippets.
"""

import html

import streamlit as st


def section_header(
    title,
    subtitle=None,
    eyebrow=None,
):
    """Render a consistent page or section header."""

    if eyebrow:
        st.caption(
            str(eyebrow).upper()
        )

    st.title(
        str(title)
    )

    if subtitle:
        st.caption(
            str(subtitle)
        )


def chip_row(items, variant="muted"):
    """Render a wrapped row of pill-style chips. variant: accent|success|danger|muted."""
    if not items:
        return
    css_class = f"ph-chip ph-chip-{variant}" if variant != "muted" else "ph-chip ph-chip-muted"
    chips_html = "".join(f'<span class="{css_class}">{html.escape(str(item))}</span>' for item in items)
    st.markdown(f'<div class="ph-chip-row">{chips_html}</div>', unsafe_allow_html=True)


def evidence_badge(level: str):
    """Return the CSS class + display label for an evidence/relevance level."""
    level = (level or "none").strip().lower()
    mapping = {
        "strong": ("ph-badge-strong", "STRONG"),
        "partial": ("ph-badge-partial", "PARTIAL"),
        "none": ("ph-badge-none", "NONE"),
    }
    return mapping.get(level, ("ph-badge-neutral", level.upper() or "UNKNOWN"))


def render_badge(level: str):
    css_class, label = evidence_badge(level)
    st.markdown(f'<span class="ph-badge {css_class}">{label}</span>', unsafe_allow_html=True)


def score_row(label, value):
    """A compact label/value row used inside score-breakdown cards."""
    try:
        display_value = f"{float(value):.0f}%"
    except (TypeError, ValueError):
        display_value = "—"

    st.markdown(
        f"""
        <div class="ph-score-row">
            <span>{html.escape(str(label))}</span>
            <span class="ph-score-value">{display_value}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    try:
        st.progress(max(0.0, min(float(value) / 100, 1.0)))
    except (TypeError, ValueError):
        st.progress(0.0)


def rank_pill(rank, gold=False):
    css = "ph-rank-pill gold" if gold else "ph-rank-pill"
    st.markdown(f'<span class="{css}">#{rank}</span>', unsafe_allow_html=True)


def empty_state(title, message, icon="📋"):
    st.markdown(
        f"""
        <div class="ph-empty">
            <div style="font-size:1.8rem; margin-bottom:0.4rem;">{icon}</div>
            <div class="ph-empty-title">{html.escape(title)}</div>
            <div>{html.escape(message)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card_start(title=None, meta=None):
    """Open a styled card container. Must be paired with card_end()."""
    st.markdown('<div class="ph-card">', unsafe_allow_html=True)
    if title:
        st.markdown(f'<div class="ph-card-title">{html.escape(title)}</div>', unsafe_allow_html=True)
    if meta:
        st.markdown(f'<div class="ph-card-meta">{html.escape(meta)}</div>', unsafe_allow_html=True)


def card_end():
    st.markdown("</div>", unsafe_allow_html=True)


def status_dot_row(label, on: bool):
    dot_class = "ph-status-dot on" if on else "ph-status-dot off"
    state_label = "Ready" if on else "Pending"
    st.markdown(
        f"""
        <div class="ph-status-row">
            <span><span class="{dot_class}"></span>{html.escape(label)}</span>
            <span>{state_label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
