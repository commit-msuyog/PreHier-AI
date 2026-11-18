import streamlit as st

from services.screening_service import screen_resume
from ui.components import chip_row, empty_state, nav_button, section_header, subheading
from ui.state import has_job_profile


def _render_candidate_card(name, profile):
    experience = profile.get("experience", {}) or {}
    years = experience.get("years", 0)
    skills = profile.get("skills", [])
    summary = f"{years} yrs" if years else "experience not stated"

    with st.expander(f"{name or 'Unnamed candidate'}  –  {summary}, {len(skills)} skills"):
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"**Email**\n\n{profile.get('email') or '—'}")
        col2.markdown(f"**Phone**\n\n{profile.get('phone') or '—'}")
        col3.markdown(f"**Experience**\n\n{f'{years} year(s)' if years else 'Not specified'}")

        for label, items, variant in [
            ("Roles", experience.get("roles", []), "muted"),
            ("Education", profile.get("education", []), "muted"),
            ("Skills", skills, "accent"),
            ("Certifications", profile.get("certifications", []), "muted"),
        ]:
            if items:
                st.markdown(f"**{label}**")
                chip_row(items, variant)

        for label, items in [("Projects", profile.get("projects", [])), ("Achievements", profile.get("achievements", []))]:
            if items:
                st.markdown(f"**{label}**")
                for item in items:
                    st.markdown(f"- {item}")

        with st.expander("View raw data"):
            st.json(profile)


def render():
    section_header(
        "Candidates",
        subtitle="Upload resumes as PDF or DOCX. Each one is read, profiled and scored against the job.",
    )

    if not has_job_profile():
        st.warning("Analyze a job description on the Job Setup page first. Screening needs it.")
        nav_button("Go to Job Setup", "job-setup", "res_job")

    uploads = st.file_uploader(
        "Upload candidate resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        help="Drag in one or more PDF or DOCX resumes.",
        label_visibility="collapsed",
    )

    # Duplicate handling: results are keyed by file name, so keep the first of each.
    resumes, seen, dupes = [], set(), []
    for upload in uploads or []:
        if upload.name in seen:
            dupes.append(upload.name)
        else:
            seen.add(upload.name)
            resumes.append(upload)
    if dupes:
        st.warning(f"Skipping duplicate file name(s): {', '.join(sorted(set(dupes)))}")

    if resumes:
        st.caption(f"{len(resumes)} resume(s) ready to analyze")
        chip_row([r.name for r in resumes], "accent")

    analyze_clicked = st.button("Analyze candidates", type="primary", disabled=not resumes or not has_job_profile())

    if analyze_clicked and resumes:
        job_profile = st.session_state.job_profile
        st.session_state.candidate_profiles = {}
        st.session_state.match_results = {}
        st.session_state.screening_errors = {}

        total, succeeded = len(resumes), 0
        progress = st.progress(0.0)

        with st.status("Analyzing candidates...", expanded=True) as status:
            for index, resume in enumerate(resumes, start=1):
                status.write(f"Reading {resume.name} ({index}/{total})...")
                try:
                    candidate_profile, match_result = screen_resume(resume, job_profile)
                except ValueError as error:
                    st.session_state.screening_errors[resume.name] = str(error)
                    status.write(f"⚠ Could not analyze {resume.name}: {error}")
                    progress.progress(index / total)
                    continue
                except Exception:
                    message = "An unexpected error occurred while analyzing this resume."
                    st.session_state.screening_errors[resume.name] = message
                    status.write(f"⚠ {resume.name}: {message}")
                    progress.progress(index / total)
                    continue

                st.session_state.candidate_profiles[resume.name] = candidate_profile
                st.session_state.match_results[resume.name] = match_result
                succeeded += 1
                progress.progress(index / total)
                status.write(f"✓ {resume.name} analyzed and scored")

            st.session_state.has_run_screening = True

            if succeeded == total:
                status.update(label=f"Analyzed all {total} resume(s).", state="complete")
            elif succeeded == 0:
                status.update(label="None of the resumes could be analyzed.", state="error")
            else:
                status.update(label=f"Analyzed {succeeded} of {total} resume(s). {total - succeeded} failed, see details below.", state="complete")
        progress.empty()

    if st.session_state.screening_errors:
        with st.expander(f"{len(st.session_state.screening_errors)} resume(s) could not be analyzed"):
            for resume_name, message in st.session_state.screening_errors.items():
                st.write(f"**{resume_name}**: {message}")

    st.divider()

    if st.session_state.candidate_profiles:
        subheading("Candidate profiles")
        c1, _ = st.columns([1, 3])
        with c1:
            nav_button("View screening results", "results", "res_view", primary=True)
        for name, profile in st.session_state.candidate_profiles.items():
            _render_candidate_card(name, profile)
    else:
        empty_state(
            "No candidates yet",
            "Drop resumes above and choose Analyze candidates. Profiles appear here.",
            icon="📄",
        )