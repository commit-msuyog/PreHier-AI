"""
PreHier design system.

A small, restrained set of CSS custom properties and component classes
that give the Streamlit app a premium, classic "enterprise HR SaaS" look
without fighting Streamlit's internals or depending on fragile DOM
selectors any more than necessary.

`inject_css()` is called once from prehier.py before any page renders.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------

COLORS = {
    "navy": "#0F2544",       # primary
    "navy_light": "#1B3A63",
    "slate": "#5B6B82",      # secondary text / neutral
    "slate_light": "#8592A6",
    "accent": "#2F5FDA",     # restrained blue/indigo accent
    "accent_soft": "#EAF0FE",
    "success": "#1E8E5A",
    "success_soft": "#E7F5EE",
    "warning": "#B7791F",
    "warning_soft": "#FBF3E3",
    "danger": "#B3261E",
    "danger_soft": "#FCEBEA",
    "bg": "#F6F8FB",
    "card": "#FFFFFF",
    "border": "#E3E8EF",
    "text": "#16233B",
}

CSS = f"""
<style>
:root {{
    --ph-navy: {COLORS['navy']};
    --ph-navy-light: {COLORS['navy_light']};
    --ph-slate: {COLORS['slate']};
    --ph-accent: {COLORS['accent']};
    --ph-accent-soft: {COLORS['accent_soft']};
    --ph-success: {COLORS['success']};
    --ph-success-soft: {COLORS['success_soft']};
    --ph-warning: {COLORS['warning']};
    --ph-warning-soft: {COLORS['warning_soft']};
    --ph-danger: {COLORS['danger']};
    --ph-danger-soft: {COLORS['danger_soft']};
    --ph-border: {COLORS['border']};
    --ph-text: {COLORS['text']};
}}

/* ---- Base layout tweaks ---------------------------------------------- */
.block-container {{
    padding-top: 2.2rem;
    max-width: 1100px;
}}

h1, h2, h3 {{
    color: var(--ph-navy);
    font-weight: 650;
    letter-spacing: -0.01em;
}}

/* ---- Sidebar brand ----------------------------------------------------- */
.ph-brand {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.25rem 0 1rem 0;
    margin-bottom: 0.25rem;
    border-bottom: 1px solid var(--ph-border);
}}
.ph-brand-mark {{
    width: 34px;
    height: 34px;
    border-radius: 8px;
    background: linear-gradient(135deg, var(--ph-navy), var(--ph-accent));
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 0.95rem;
    flex-shrink: 0;
}}
.ph-brand-text .ph-brand-title {{
    font-weight: 700;
    font-size: 1.05rem;
    color: var(--ph-navy);
    line-height: 1.1;
}}
.ph-brand-text .ph-brand-subtitle {{
    font-size: 0.72rem;
    color: var(--ph-slate);
    letter-spacing: 0.02em;
    text-transform: uppercase;
}}

.ph-status-list {{
    font-size: 0.85rem;
    color: var(--ph-slate);
    padding-top: 0.4rem;
}}
.ph-status-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.15rem 0;
}}
.ph-status-dot {{
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 6px;
}}
.ph-status-dot.on {{ background: var(--ph-success); }}
.ph-status-dot.off {{ background: #C7CDD8; }}

/* ---- Section header ----------------------------------------------------- */
.ph-section-header {{
    margin-bottom: 0.35rem;
}}
.ph-section-header .ph-eyebrow {{
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--ph-accent);
    margin-bottom: 0.15rem;
}}
.ph-section-header .ph-title {{
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--ph-navy);
    margin: 0;
}}
.ph-section-header .ph-subtitle {{
    color: var(--ph-slate);
    font-size: 0.95rem;
    margin-top: 0.2rem;
}}

/* ---- Cards --------------------------------------------------------------- */
.ph-card {{
    background: var(--ph-card, #fff);
    border: 1px solid var(--ph-border);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 2px rgba(15, 37, 68, 0.04);
}}
.ph-card-title {{
    font-weight: 700;
    font-size: 1.05rem;
    color: var(--ph-navy);
    margin-bottom: 0.15rem;
}}
.ph-card-meta {{
    color: var(--ph-slate);
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
}}

/* ---- Chips / badges -------------------------------------------------- */
.ph-chip-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin: 0.25rem 0 0.6rem 0;
}}
.ph-chip {{
    display: inline-block;
    padding: 0.22rem 0.7rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 500;
    border: 1px solid var(--ph-border);
    background: #F3F5F8;
    color: var(--ph-text);
    white-space: nowrap;
}}
.ph-chip-accent {{
    background: var(--ph-accent-soft);
    border-color: #C9D8FA;
    color: var(--ph-navy);
}}
.ph-chip-success {{
    background: var(--ph-success-soft);
    border-color: #BFE3D1;
    color: var(--ph-success);
}}
.ph-chip-danger {{
    background: var(--ph-danger-soft);
    border-color: #F1C6C3;
    color: var(--ph-danger);
}}
.ph-chip-muted {{
    background: #F3F5F8;
    color: var(--ph-slate);
}}

.ph-badge {{
    display: inline-block;
    padding: 0.15rem 0.55rem;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}}
.ph-badge-strong {{ background: var(--ph-success-soft); color: var(--ph-success); }}
.ph-badge-partial {{ background: var(--ph-warning-soft); color: var(--ph-warning); }}
.ph-badge-none {{ background: var(--ph-danger-soft); color: var(--ph-danger); }}
.ph-badge-neutral {{ background: #EEF1F5; color: var(--ph-slate); }}

/* ---- Score rows -------------------------------------------------------- */
.ph-score-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.85rem;
    color: var(--ph-text);
    margin-top: 0.55rem;
    margin-bottom: 0.1rem;
}}
.ph-score-row .ph-score-value {{
    font-weight: 700;
    color: var(--ph-navy);
}}

/* ---- Rank pill ----------------------------------------------------------- */
.ph-rank-pill {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 28px;
    height: 28px;
    padding: 0 6px;
    border-radius: 8px;
    background: var(--ph-navy);
    color: white;
    font-weight: 700;
    font-size: 0.85rem;
    margin-right: 0.5rem;
}}
.ph-rank-pill.gold {{ background: #B5891A; }}

/* ---- Empty state --------------------------------------------------------- */
.ph-empty {{
    text-align: center;
    padding: 2.6rem 1.5rem;
    border: 1px dashed var(--ph-border);
    border-radius: 14px;
    color: var(--ph-slate);
    background: #FBFCFE;
}}
.ph-empty .ph-empty-title {{
    font-weight: 700;
    color: var(--ph-navy);
    font-size: 1.1rem;
    margin-bottom: 0.3rem;
}}

/* ---- Streamlit widget polish ------------------------------------------- */
div[data-testid="stMetric"] {{
    background: var(--ph-card, #fff);
    border: 1px solid var(--ph-border);
    border-radius: 12px;
    padding: 0.85rem 1rem 0.7rem 1rem;
    box-shadow: 0 1px 2px rgba(15, 37, 68, 0.04);
}}
div[data-testid="stMetricLabel"] {{
    color: var(--ph-slate);
}}

button[kind="primary"] {{
    background-color: var(--ph-navy);
    border-color: var(--ph-navy);
}}
button[kind="primary"]:hover {{
    background-color: var(--ph-navy-light);
    border-color: var(--ph-navy-light);
}}

hr {{
    border-color: var(--ph-border);
}}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)
