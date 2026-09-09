import streamlit as st
from pypdf import PdfReader

from src.ai.job_analyzer import analyze_job_description
from src.ai.candidate_analyzer import analyze_candidate
from src.screening.matching_engine import (
    calculate_skill_match,
    calculate_preferred_skill_match
)
from src.screening.scoring_engine import (
    calculate_experience_score,
    calculate_education_score,
    calculate_overall_score,
    relevance_to_score
)
from src.screening.evidence_matcher import evaluate_requirement_evidence
from src.screening.project_matcher import evaluate_project_relevance
from src.screening.ranking_engine import rank_candidates
from src.screening.shortlist_engine import create_shortlist


st.set_page_config(
    page_title="PreHier",
    page_icon="🎯",
    layout="centered"
)

if "job_profile" not in st.session_state:
    st.session_state.job_profile = None

if "candidate_profiles" not in st.session_state:
    st.session_state.candidate_profiles = {}

if "match_results" not in st.session_state:
    st.session_state.match_results = {}

if "selected_candidates" not in st.session_state:
    st.session_state.selected_candidates = []

st.title("🎯 PreHier")
st.subheader("AI-Powered Pre-Hire Screening")
st.write(
    "Screen and shortlist candidates based on your job requirements."
)

st.divider()

st.header("💼 Job Description")

job_description = st.text_area(
    "Paste the job description here",
    placeholder="Paste the job description of the role you are hiring for...",
    height=250
)

if job_description:
    if st.button("Analyze Job Description"):
        with st.spinner("Analyzing job description..."):
            st.session_state.job_profile = analyze_job_description(
                job_description
            )

        st.subheader("💼 Job Profile")
        st.json(st.session_state.job_profile)

st.divider()

st.header("📄 Candidate Resumes")

resumes = st.file_uploader(
    "Upload candidate resumes",
    type=["pdf"],
    accept_multiple_files=True,
    help="Upload one or more candidate resumes in PDF format."
)

if resumes:
    st.success(
        f"{len(resumes)} candidate resume(s) uploaded."
    )

    if st.button(
        "🚀 Analyze All Resumes",
        type="primary"
    ):
        if not st.session_state.job_profile:
            st.warning(
                "Please analyze the job description first."
            )
        else:
            st.session_state.candidate_profiles = {}
            st.session_state.match_results = {}

            progress_bar = st.progress(0)
            status_text = st.empty()

            total_resumes = len(resumes)

            for index, resume in enumerate(resumes):

                status_text.write(
                    f"Analyzing {resume.name} "
                    f"({index + 1}/{total_resumes})..."
                )

                reader = PdfReader(resume)
                resume_text = ""

                for page in reader.pages:
                    text = page.extract_text()

                    if text:
                        resume_text += text + "\n"

                candidate_profile = analyze_candidate(
                    resume_text
                )

                st.session_state.candidate_profiles[
                    resume.name
                ] = candidate_profile

                required_experience = (
                    st.session_state.job_profile[
                        "experience_required"
                    ]
                )

                required_years = required_experience.get(
                    "years",
                    0
                )

                candidate_years = (
                    candidate_profile[
                        "experience"
                    ].get(
                        "years",
                        0
                    )
                )

                experience_score = calculate_experience_score(
                    required_years,
                    candidate_years
                )

                required_result = calculate_skill_match(
                    st.session_state.job_profile[
                        "required_skills"
                    ],
                    candidate_profile["skills"]
                )

                preferred_result = calculate_preferred_skill_match(
                    st.session_state.job_profile[
                        "preferred_skills"
                    ],
                    candidate_profile["skills"]
                )

                evidence_result = evaluate_requirement_evidence(
                    st.session_state.job_profile[
                        "required_skills"
                    ],
                    candidate_profile
                )

                project_result = evaluate_project_relevance(
                    st.session_state.job_profile,
                    candidate_profile["projects"]
                )

                project_relevance_score = relevance_to_score(
                    project_result.get(
                        "overall_relevance",
                        "none"
                    )
                )

                education_score = calculate_education_score(
                    st.session_state.job_profile[
                        "education"
                    ],
                    candidate_profile[
                        "education"
                    ]
                )

                overall_score = calculate_overall_score(
                    required_result["score"],
                    preferred_result["score"],
                    experience_score,
                    education_score,
                    project_relevance_score
                )

                st.session_state.match_results[
                    resume.name
                ] = {
                    "required_skills": required_result,
                    "preferred_skills": preferred_result,
                    "experience_score": experience_score,
                    "education_score": education_score,
                    "project_relevance_score": project_relevance_score,
                    "overall_score": overall_score,
                    "evidence": evidence_result,
                    "projects": project_result
                }

                progress_bar.progress(
                    (index + 1) / total_resumes
                )

            status_text.success(
                f"Successfully analyzed {total_resumes} resume(s)."
            )

st.divider()

if st.session_state.candidate_profiles:

    st.header("👥 Candidate Profiles")

    for candidate_name, candidate_profile in (
        st.session_state.candidate_profiles.items()
    ):
        with st.expander(
            f"👤 {candidate_name}"
        ):
            st.json(candidate_profile)

st.divider()

if st.session_state.match_results:

    st.header("📊 Screening Results")

    for candidate_name, result in (
        st.session_state.match_results.items()
    ):
        st.subheader(
            f"📄 {candidate_name}"
        )

        st.metric(
            "Overall Match Score",
            f"{result['overall_score']}%"
        )

        st.write("### Score Breakdown")

        st.write(
            f"Required Skills: "
            f"**{result['required_skills']['score']}%**"
        )

        st.write(
            f"Preferred Skills: "
            f"**{result['preferred_skills']['score']}%**"
        )

        st.write(
            f"Experience: "
            f"**{result['experience_score']}%**"
        )

        st.write(
            f"Education: "
            f"**{result['education_score']}%**"
        )

        st.write(
            f"Project Relevance: "
            f"**{result['project_relevance_score']}%**"
        )

        st.write("### 🎯 Skill Screening")

        required_result = result["required_skills"]

        st.write(
            "**Matched Required Skills**"
        )

        if required_result["matched_skills"]:
            st.write(
                required_result["matched_skills"]
            )
        else:
            st.write(
                "No required skills matched."
            )

        st.write(
            "**Missing Required Skills**"
        )

        if required_result["missing_skills"]:
            st.write(
                required_result["missing_skills"]
            )
        else:
            st.write(
                "No required skills are missing."
            )

        preferred_result = result["preferred_skills"]

        st.write(
            "**Matched Preferred Skills**"
        )

        if preferred_result["matched"]:
            st.write(
                preferred_result["matched"]
            )
        else:
            st.write(
                "No preferred skills matched."
            )

        st.write(
            "**Missing Preferred Skills**"
        )

        if preferred_result["missing"]:
            st.write(
                preferred_result["missing"]
            )
        else:
            st.write(
                "No preferred skills are missing."
            )

        st.write("### 🧠 Requirement Evidence")

        evidence_result = result["evidence"]

        if "requirements" in evidence_result:

            for requirement in evidence_result[
                "requirements"
            ]:
                skill = requirement.get(
                    "skill",
                    ""
                )

                level = requirement.get(
                    "evidence_level",
                    "none"
                )

                evidence = requirement.get(
                    "evidence",
                    ""
                )

                st.write(
                    f"**{skill} — "
                    f"{level.upper()}**"
                )

                if evidence:
                    st.caption(
                        f"Evidence: {evidence}"
                    )
                else:
                    st.caption(
                        "No evidence found."
                    )

        else:
            st.warning(
                "Could not evaluate candidate evidence."
            )

        st.write("### 📁 Project Relevance")

        project_result = result["projects"]

        if "projects" in project_result:

            st.write(
                f"**Overall Project Relevance: "
                f"{project_result.get(
                    'overall_relevance',
                    'unknown'
                ).upper()}**"
            )

            for project in project_result[
                "projects"
            ]:
                title = project.get(
                    "title",
                    "Unnamed Project"
                )

                relevance = project.get(
                    "relevance",
                    "none"
                )

                reason = project.get(
                    "reason",
                    ""
                )

                st.write(
                    f"**{title} — "
                    f"{relevance.upper()}**"
                )

                if reason:
                    st.caption(
                        f"Reason: {reason}"
                    )

        else:
            st.warning(
                "Could not evaluate project relevance."
            )

st.divider()

st.header("🏆 Candidate Ranking")

if st.session_state.match_results:

    ranked_candidates = rank_candidates(
        st.session_state.match_results
    )

    for candidate in ranked_candidates:

        candidate_name = candidate["candidate"]
        score = candidate["score"]

        st.write(
            f"**#{candidate['rank']} — "
            f"{candidate_name}**"
        )

        st.progress(
            min(score / 100, 1.0)
        )

        st.caption(
            f"Overall Match Score: {score}%"
        )

        if candidate_name in st.session_state.selected_candidates:
            st.success("⭐ Shortlisted")
        else:
            if st.button(
                "⭐ Shortlist",
                key=f"shortlist_{candidate_name}"
            ):
                st.session_state.selected_candidates.append(
                    candidate_name
                )
                st.rerun()

else:
    st.info(
        "Analyze resumes to generate the candidate ranking."
    )

st.divider()

st.header("⭐ Shortlisted Candidates")

if st.session_state.match_results:

    ranked_candidates = rank_candidates(
        st.session_state.match_results
    )

    shortlist = create_shortlist(
        ranked_candidates,
        st.session_state.selected_candidates
    )

    if shortlist:

        for candidate in shortlist:

            st.write(
                f"**#{candidate['rank']} — "
                f"{candidate['candidate']}**"
            )

            st.caption(
                f"Overall Match Score: "
                f"{candidate['score']}%"
            )

    else:
        st.info(
            "No candidates have been shortlisted yet."
        )

else:
    st.info(
        "Analyze resumes before creating a shortlist."
    )