"""PreHier design system: pine + amber 'evidence ledger'.

Tokens -> base -> shell -> components. inject_css() is called once from prehier.py.
Fonts: Bricolage Grotesque (headings, numbers) + Figtree (UI text), via Google Fonts.
"""

import streamlit as st

COLORS = {
    "bg": "#F1F4F1", "card": "#FFFFFF", "line": "#DCE3DF", "track": "#E4EAE6",
    "text": "#1B2A28", "muted": "#5A6B67", "faint": "#8A9A96",
    "pine": "#0B4F4A", "pine-2": "#12665F", "deep": "#072F2C",
    "mint": "#DDEFEA", "amber": "#E8A317", "amber-soft": "#FCF2D9",
    "good": "#1F8A5B", "good-soft": "#E3F4EC",
    "mid": "#B7791F", "mid-soft": "#FBF1DB",
    "bad": "#BE3A30", "bad-soft": "#FBE9E7",
}

_FONTS = "@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Figtree:wght@400;500;600;700&display=swap');\n"


def _root_vars() -> str:
    lines = [f"  --ph-{k}: {v};" for k, v in COLORS.items()]
    return ":root {\n" + "\n".join(lines) + "\n  --ph-head: 'Bricolage Grotesque','Figtree',system-ui,sans-serif;\n}\n"


_BODY = """
/* ===== Base ===== */
.stApp { background: var(--ph-bg); font-family: 'Figtree','Segoe UI',system-ui,sans-serif; }
[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1180px; }
h1,h2,h3,h4 { font-family: var(--ph-head); color: var(--ph-deep); letter-spacing: -0.015em; font-weight: 700; }
hr { border-color: var(--ph-line); }
[data-testid="stMain"] [data-testid="stMarkdownContainer"] p,
[data-testid="stMain"] label,
[data-testid="stMain"] [data-testid="stWidgetLabel"] p { color: var(--ph-text); }
[data-testid="stMain"] [data-testid="stCaptionContainer"] { color: var(--ph-muted); }
:focus-visible { outline: 2px solid var(--ph-amber) !important; outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }

/* ===== Page header ===== */
.ph-section-header { margin-bottom: 1.2rem; }
.ph-title { font-family: var(--ph-head); font-size: 2rem; font-weight: 700; color: var(--ph-deep); letter-spacing: -0.02em; line-height: 1.15; }
.ph-subtitle { color: var(--ph-muted); font-size: 1rem; margin-top: 0.3rem; max-width: 68ch; }
.ph-eyebrow { font-size: 0.8rem; font-weight: 600; color: var(--ph-pine-2); margin-bottom: 0.2rem; }
.ph-h { font-family: var(--ph-head); font-weight: 700; color: var(--ph-deep); font-size: 1.15rem; margin: 1.4rem 0 0.5rem; }
.ph-note { color: var(--ph-muted); font-size: 0.88rem; }

/* ===== Sidebar shell ===== */
section[data-testid="stSidebar"] { background: linear-gradient(180deg, var(--ph-deep) 0%, #05211F 100%); border-right: 0; }
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
section[data-testid="stSidebar"] hr { color: #CFE3DF; border-color: rgba(255,255,255,.1); }
[data-testid="stSidebarNavLink"] { border-radius: 8px; color: #CFE3DF; transition: background .15s; }
[data-testid="stSidebarNavLink"] span { color: #CFE3DF !important; font-weight: 500; }
[data-testid="stSidebarNavLink"]:hover { background: rgba(255,255,255,.07); }
[data-testid="stSidebarNavLink"][aria-current="page"] { background: rgba(232,163,23,.16); box-shadow: inset 3px 0 0 var(--ph-amber); }
[data-testid="stSidebarNavLink"][aria-current="page"] span { color: #FFFFFF !important; font-weight: 600; }

[data-testid="stSidebarHeader"] { padding: 1.4rem 1rem 1rem; }
[data-testid="stSidebarHeader"] img { height: 2.8rem; width: auto; }
[data-testid="stSidebarNav"] { padding-bottom: 0; margin-bottom: 0; }
[data-testid="stSidebarUserContent"] { padding-top: 0 !important; }
[data-testid="stSidebarUserContent"] hr { margin: 0.6rem 0; }

.ph-brand { display: flex; align-items: flex-end; gap: .7rem; padding: .3rem 0 .2rem; }
.ph-mark { display: flex; align-items: flex-end; gap: 3px; height: 30px; }
.ph-mark i { display: block; width: 7px; border-radius: 2px; background: #7FC9BD; }
.ph-mark i:nth-child(1) { height: 12px; } .ph-mark i:nth-child(2) { height: 20px; } .ph-mark i:nth-child(3) { height: 30px; background: var(--ph-amber); }
.ph-brand-title { font-family: var(--ph-head); font-weight: 700; font-size: 1.9rem; color: #FFF; line-height: 1; }
.ph-brand-subtitle { font-size: .78rem; color: #9DB8B2; margin-top: .25rem; }
.ph-status-row { display: flex; justify-content: space-between; align-items: center; padding: .4rem 0; font-size: .88rem; color: #CFE3DF; border-bottom: 1px solid rgba(255,255,255,.08); }
.ph-status-row:last-child { border-bottom: 0; }
.ph-status-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: .55rem; }
.ph-status-dot.on { background: #4BD39B; box-shadow: 0 0 0 3px rgba(75,211,155,.18); }
.ph-status-dot.off { background: #6F8A85; }
.ph-sidebar-developer { padding-top: 2rem; }
.ph-sidebar-developer-name { font-size: .88rem; font-weight: 700; color: #EAF6F3; }
.ph-sidebar-developer-quote { font-size: .76rem; font-style: italic; color: #9DB8B2; margin-top: .2rem; }

/* ===== Cards ===== */
div[data-testid="stVerticalBlockBorderWrapper"] { background: var(--ph-card); border-color: var(--ph-line) !important; border-radius: 12px; }
.ph-card-title { font-family: var(--ph-head); font-weight: 700; font-size: 1.05rem; color: var(--ph-deep); }
.ph-card-meta { color: var(--ph-muted); font-size: .85rem; margin-bottom: .4rem; }
.ph-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: .75rem; margin-bottom: .5rem; }
.ph-tile { background: var(--ph-card); border: 1px solid var(--ph-line); border-radius: 12px; padding: .9rem 1rem; }
.ph-tile-label { font-size: .82rem; color: var(--ph-muted); font-weight: 500; }
.ph-tile-value { font-family: var(--ph-head); font-size: 1.9rem; font-weight: 700; color: var(--ph-deep); line-height: 1.15; }
.ph-tile-note { font-size: .8rem; color: var(--ph-faint); }

/* ===== Chips & badges ===== */
.ph-chip-row { display: flex; flex-wrap: wrap; gap: .4rem; margin: .25rem 0 .7rem; }
.ph-chip { display: inline-block; padding: .2rem .7rem; border-radius: 999px; font-size: .82rem; font-weight: 500; border: 1px solid var(--ph-line); background: #F3F6F4; color: var(--ph-text); }
.ph-chip-accent { background: var(--ph-mint); border-color: #B9DDD5; color: var(--ph-deep); }
.ph-chip-success { background: var(--ph-good-soft); border-color: #BFE3D1; color: var(--ph-good); }
.ph-chip-warning { background: var(--ph-mid-soft); border-color: #EBD7A8; color: var(--ph-mid); }
.ph-chip-danger { background: var(--ph-bad-soft); border-color: #F1C6C3; color: var(--ph-bad); }
.ph-chip-muted { color: var(--ph-muted); }
.ph-badge { display: inline-block; padding: .15rem .55rem; border-radius: 6px; font-size: .75rem; font-weight: 700; white-space: nowrap; }
.ph-badge-strong { background: var(--ph-good-soft); color: var(--ph-good); }
.ph-badge-partial { background: var(--ph-mid-soft); color: var(--ph-mid); }
.ph-badge-none { background: var(--ph-bad-soft); color: var(--ph-bad); }
.ph-badge-neutral { background: #EEF1F0; color: var(--ph-muted); }

/* ===== Score language: ring + strip ===== */
.ph-ring { --v: 0; --c: var(--ph-good); --s: 64px; width: var(--s); height: var(--s); border-radius: 50%; flex-shrink: 0;
  background: conic-gradient(var(--c) calc(var(--v) * 1%), var(--ph-track) 0); display: grid; place-items: center; }
.ph-ring > span { width: calc(100% - 12px); height: calc(100% - 12px); border-radius: 50%; background: #FFF; display: grid; place-items: center;
  font-family: var(--ph-head); font-weight: 700; font-size: calc(var(--s) * .32); color: var(--ph-deep); }
.b-high { --c: var(--ph-good); } .b-mid { --c: var(--ph-amber); } .b-low { --c: var(--ph-bad); }
.ph-strip { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: .6rem; margin-top: .6rem; }
.ph-seg { font-size: .76rem; color: var(--ph-muted); }
.ph-seg-bar { height: 8px; border-radius: 4px; background: var(--ph-track); overflow: hidden; margin-bottom: .3rem; }
.ph-seg-bar i { display: block; height: 100%; background: var(--c); border-radius: 4px; }
.ph-seg b { display: block; color: var(--ph-deep); font-size: .9rem; }
.ph-fit { font-size: .8rem; font-weight: 700; padding: .15rem .55rem; border-radius: 6px; }
.ph-fit.b-high { background: var(--ph-good-soft); color: var(--ph-good); }
.ph-fit.b-mid { background: var(--ph-mid-soft); color: var(--ph-mid); }
.ph-fit.b-low { background: var(--ph-bad-soft); color: var(--ph-bad); }
.ph-rank-pill { display: inline-flex; align-items: center; justify-content: center; min-width: 30px; height: 30px; padding: 0 7px; border-radius: 8px; background: var(--ph-deep); color: #FFF; font-family: var(--ph-head); font-weight: 700; font-size: .88rem; margin-right: .6rem; }
.ph-rank-pill.gold { background: var(--ph-amber); color: var(--ph-deep); }
.ph-cand { display: flex; align-items: center; gap: .6rem; flex-wrap: wrap; }
.ph-cand-name { font-family: var(--ph-head); font-weight: 700; font-size: 1.1rem; color: var(--ph-deep); overflow-wrap: anywhere; }

/* ===== Hero (the one bold surface) ===== */
.ph-hero { background: linear-gradient(135deg, var(--ph-deep), var(--ph-pine)); border-radius: 16px; padding: 1.4rem 1.6rem; color: #FFF; }
.ph-hero-top { display: flex; gap: 1.2rem; align-items: center; flex-wrap: wrap; }
.ph-hero .lbl { font-size: .85rem; color: #A9D3CB; font-weight: 600; }
.ph-hero .nm { font-family: var(--ph-head); font-size: 1.75rem; font-weight: 700; line-height: 1.15; overflow-wrap: anywhere; }
.ph-hero .ph-ring { --s: 92px; background: conic-gradient(var(--ph-amber) calc(var(--v) * 1%), rgba(255,255,255,.16) 0); }
.ph-hero .ph-ring > span { background: var(--ph-deep); color: #FFF; }
.ph-hero .ph-seg { color: #A9D3CB; } .ph-hero .ph-seg b { color: #FFF; }
.ph-hero .ph-seg-bar { background: rgba(255,255,255,.16); } .ph-hero .ph-seg-bar i { background: var(--ph-amber); }

/* ===== Bars / lists / tables ===== */
.ph-bar-row { display: grid; grid-template-columns: 9.5rem 1fr 2.2rem; gap: .7rem; align-items: center; padding: .35rem 0; font-size: .9rem; color: var(--ph-text); }
.ph-bar { height: 10px; border-radius: 5px; background: var(--ph-track); overflow: hidden; } .ph-bar i { display: block; height: 100%; border-radius: 5px; background: var(--c, var(--ph-pine-2)); }
.ph-bar-row b { text-align: right; color: var(--ph-deep); }
.ph-ev { display: flex; justify-content: space-between; gap: 1rem; padding: .6rem 0; border-bottom: 1px solid var(--ph-line); }
.ph-ev:last-child { border-bottom: 0; } .ph-ev b { color: var(--ph-deep); } .ph-ev p { margin: .15rem 0 0; color: var(--ph-muted); font-size: .86rem; }
.ph-insights { margin: .4rem 0 .2rem; padding-left: 1.1rem; color: var(--ph-text); } .ph-insights li { margin-bottom: .25rem; }
.ph-table-wrap { overflow-x: auto; border: 1px solid var(--ph-line); border-radius: 12px; background: #FFF; }
.ph-table { width: 100%; border-collapse: collapse; font-size: .9rem; }
.ph-table th { text-align: left; padding: .8rem 1rem; color: var(--ph-deep); font-family: var(--ph-head); border-bottom: 1px solid var(--ph-line); white-space: nowrap; }
.ph-table td { padding: .65rem 1rem; border-bottom: 1px solid #EEF2EF; color: var(--ph-text); min-width: 150px; }
.ph-table tr:last-child td { border-bottom: 0; } .ph-table td.dim { color: var(--ph-muted); font-weight: 600; min-width: 130px; }
.ph-table td.best { background: var(--ph-good-soft); } .ph-table td.best .v::after { content: ' best'; font-size: .72rem; color: var(--ph-good); font-weight: 700; }
.ph-table .v { font-weight: 700; color: var(--ph-deep); }
.ph-empty { text-align: center; padding: 2.6rem 1.5rem; border: 1px dashed #B9C8C3; border-radius: 14px; color: var(--ph-muted); background: #F8FAF8; }
.ph-empty .ph-empty-title { font-family: var(--ph-head); font-weight: 700; color: var(--ph-deep); font-size: 1.15rem; margin-bottom: .3rem; }

/* ===== Native widgets ===== */
[data-testid="stMain"] input, [data-testid="stMain"] textarea { color: var(--ph-text) !important; -webkit-text-fill-color: var(--ph-text) !important; }
[data-testid="stMain"] div[data-baseweb="input"], [data-testid="stMain"] div[data-baseweb="textarea"], [data-testid="stMain"] div[data-baseweb="select"] > div { background: #FFF; border-color: var(--ph-line); border-radius: 10px; }
[data-testid="stMain"] div[data-baseweb="input"]:focus-within, [data-testid="stMain"] div[data-baseweb="textarea"]:focus-within { border-color: var(--ph-pine-2); box-shadow: 0 0 0 3px var(--ph-mint); }
[data-testid="stFileUploaderDropzone"] { background: #F8FAF8; border: 1.5px dashed #9DB8B2; border-radius: 14px; padding: 1.6rem; }
button[kind="primary"], button[data-testid="stBaseButton-primary"] { background: var(--ph-pine); border-color: var(--ph-pine); border-radius: 10px; font-weight: 600; transition: background .15s; }
button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover { background: var(--ph-pine-2); border-color: var(--ph-pine-2); }
button[kind="primary"] p, button[data-testid="stBaseButton-primary"] p { color: #FFF !important; }
[data-testid="stMain"] button[kind="secondary"], [data-testid="stMain"] button[data-testid="stBaseButton-secondary"] { border-radius: 10px; border-color: var(--ph-line); background: #FFF; }
[data-testid="stMain"] button[kind="secondary"]:hover { border-color: var(--ph-pine-2); color: var(--ph-pine-2); }
button[data-baseweb="tab"] p { color: var(--ph-muted); font-weight: 600; }
button[data-baseweb="tab"][aria-selected="true"] p { color: var(--ph-deep); }
div[data-baseweb="tab-highlight"] { background-color: var(--ph-amber) !important; }
[data-testid="stExpander"] { background: #FFF; border: 1px solid var(--ph-line); border-radius: 12px; }
[data-testid="stAlert"] { border-radius: 12px; }
[data-testid="stDataFrame"] { border: 1px solid var(--ph-line); border-radius: 12px; overflow: hidden; }
@media (max-width: 780px) { .ph-strip { grid-template-columns: repeat(3, minmax(0,1fr)); } .ph-bar-row { grid-template-columns: 6.5rem 1fr 2rem; } .ph-title { font-size: 1.6rem; } }
"""

CSS = "<style>\n" + _FONTS + _root_vars() + _BODY + "\n</style>"


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)