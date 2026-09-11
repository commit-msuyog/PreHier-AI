import streamlit as st

from services.screening_service import screen_resume
from ui.components import chip_row, empty_state, section_header
from ui.state import has_job_profile


def _render_candidate_card(name, profile):
    email = profile.get("email") or "—"
    phone = profile.get("phone") or "—"
    experience = profile.get("experience", {}) or {}
    years = experience.get("years", 0)

    with st.expander(f"{name or 'Unnamed candidate'}"):
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"**Email**\n\n{email}")
        col2.markdown(f"**Phone**\n\n{phone}")
        col3.markdown(f"**Experience**\n\n{years} year(s)" if years else "**Experience**\n\nNot specified")

        roles = experience.get("roles", [])
        if roles:
            st.markdown("**Roles**")
            chip_row(roles, variant="muted")

        education = profile.get("education", [])
        if education:
            st.markdown("**Education**")
            chip_row(education, variant="muted")

        skills = profile.get("skills", [])
        if skills:
            st.markdown("**Skills**")
            chip_row(skills, variant="accent")

        projects = profile.get("projects", [])
        if projects:
            st.markdown("**Projects**")
            for project in projects:
                st.markdown(f"- {project}")

        certifications = profile.get("certifications", [])
        if certifications:
            st.markdown("**Certifications**")
            chip_row(certifications, variant="muted")

        achievements = profile.get("achievements", [])
        if achievements:
            st.markdown("**Achievements**")
            for achievement in achievements:
                st.markdown(f"- {achievement}")

        with st.expander("View raw data"):
            st.json(profile)


def render():
    section_header(
        "Candidates",
        subtitle="Upload candidate resumes as PDF files, then run AI analysis against the job profile.",
        eyebrow="Step 2",
    )

    if not has_job_profile():
        st.warning(
            "Analyze a job description on the Job Setup page before "
            "screening candidates."
        )

    resumes = st.file_uploader(
        "Upload candidate resumes",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more candidate resumes in PDF format.",
    )

    if resumes:
        st.caption(f"{len(resumes)} file(s) ready to analyze")
        chip_row([resume.name for resume in resumes], variant="muted")

    analyze_clicked = st.button(
        "Analyze Candidates",
        type="primary",
        disabled=not resumes or not has_job_profile(),
    )

    if analyze_clicked and resumes:
        job_profile = st.session_state.job_profile

        st.session_state.candidate_profiles = {}
        st.session_state.match_results = {}
        st.session_state.screening_errors = {}

        total = len(resumes)
        succeeded = 0

        with st.status("Analyzing candidates...", expanded=True) as status:
            for index, resume in enumerate(resumes, start=1):
                status.write(f"Reading {resume.name} ({index}/{total})...")

                try:
                    candidate_profile, match_result = screen_resume(resume, job_profile)
                except ValueError as error:
                    st.session_state.screening_errors[resume.name] = str(error)
                    status.write(f"⚠ Could not analyze {resume.name}: {error}")
                    continue
                except Exception:
                    friendly_message = (
                        "An unexpected error occurred while analyzing this resume."
                    )
                    st.session_state.screening_errors[resume.name] = friendly_message
                    status.write(f"⚠ {resume.name}: {friendly_message}")
                    continue

                st.session_state.candidate_profiles[resume.name] = candidate_profile
                st.session_state.match_results[resume.name] = match_result
                succeeded += 1
                status.write(f"✓ {resume.name} analyzed and scored")

            st.session_state.has_run_screening = True

            if succeeded == total:
                status.update(
                    label=f"Analyzed {succeeded} of {total} resume(s) successfully.",
                    state="complete",
                )
            elif succeeded == 0:
                status.update(
                    label="Could not analyze any of the uploaded resumes.",
                    state="error",
                )
            else:
                status.update(
                    label=f"Analyzed {succeeded} of {total} resume(s). "
                          f"{total - succeeded} failed — see details above.",
                    state="complete",
                )

    if st.session_state.screening_errors:
        with st.expander(
            f"{len(st.session_state.screening_errors)} resume(s) could not be analyzed",
            expanded=False,
        ):
            for resume_name, message in st.session_state.screening_errors.items():
                st.write(f"**{resume_name}** — {message}")

    st.divider()

    if st.session_state.candidate_profiles:
        st.markdown("### Candidate Profiles")
        for name, profile in st.session_state.candidate_profiles.items():
            _render_candidate_card(name, profile)
    else:
        empty_state(
            "No candidates analyzed yet",
            "Upload one or more PDF resumes above and click \"Analyze Candidates\" "
            "to generate structured candidate profiles.",
            icon="📄",
        )
