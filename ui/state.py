"""
Centralized Streamlit session_state management for PreHier.

All screening data (job profile, candidate profiles, match results,
shortlist selections) lives in st.session_state so that it survives
navigation between pages in Streamlit's multipage architecture.

`init_session_state()` is idempotent: it only sets a key the first time
it is missing, so calling it at the top of every page render is safe and
never resets data a recruiter has already produced.
"""

import streamlit as st

DEFAULTS = {
    # The analyzed job requirements (dict) or None if not yet analyzed.
    "job_profile": None,

    # The raw job description text the recruiter last submitted, kept so
    # the textarea is repopulated when navigating back to Job Setup.
    "job_description_text": "",

    # candidate_name -> candidate_profile (dict extracted from the resume)
    "candidate_profiles": {},

    # candidate_name -> match_result (scores, evidence, project relevance)
    "match_results": {},

    # List of candidate names the recruiter has shortlisted.
    "selected_candidates": [],

    # candidate_name -> friendly error message, for resumes that failed
    # to analyze. Cleared at the start of each new analysis run.
    "screening_errors": {},

    # Set to True once at least one "Analyze Candidates" run has finished,
    # so pages can distinguish "never run" from "ran with zero results".
    "has_run_screening": False,
}


def init_session_state():
    """Populate st.session_state with defaults for any missing keys."""
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            # Use a fresh copy for mutable defaults (dict/list) so pages
            # don't accidentally share the same object across sessions.
            st.session_state[key] = value.copy() if isinstance(value, (dict, list)) else value


def has_job_profile() -> bool:
    profile = st.session_state.get("job_profile")
    return bool(profile) and "error" not in profile


def has_candidates() -> bool:
    return bool(st.session_state.get("match_results"))
