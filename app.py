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

# Page configuration

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

# Header

st.title("🎯 PreHier")
st.subheader("AI-Powered Pre-Hire Screening")
st.write(
    "Screen and shortlist candidates based on your job requirements."
)
st.divider()

# Job description

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

# Candidate resumes

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

    for resume in resumes:
        st.divider()
        st.subheader(f"📄 {resume.name}")

        # Extract resume text

        reader = PdfReader(resume)
        resume_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                resume_text += text + "\n"

        # Show extracted resume text

        with st.expander("View Extracted Resume Text"):
            st.text_area(
                "Resume Content",
                resume_text,
                height=250,
                key=f"text_{resume.name}"
            )

        # Analyze candidate

        if st.button(
            f"Analyze {resume.name}",
            key=f"analyze_{resume.name}"
        ):
            with st.spinner(
                f"Analyzing {resume.name}..."
            ):
                candidate_profile = analyze_candidate(
                    resume_text
                )

                st.session_state.candidate_profiles[
                    resume.name
                ] = candidate_profile

            st.subheader("👤 Candidate Profile")
            st.json(candidate_profile)

            if st.session_state.job_profile:

                # Calculate experience score

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

                # Calculate required skill match

                required_result = calculate_skill_match(
                    st.session_state.job_profile[
                        "required_skills"
                    ],
                    candidate_profile["skills"]
                )

                # Calculate preferred skill match

                preferred_result = calculate_preferred_skill_match(
                    st.session_state.job_profile[
                        "preferred_skills"
                    ],
                    candidate_profile["skills"]
                )

                # Evaluate requirement evidence

                with st.spinner(
                    "Evaluating candidate evidence..."
                ):
                    evidence_result = (
                        evaluate_requirement_evidence(
                            st.session_state.job_profile[
                                "required_skills"
                            ],
                            candidate_profile
                        )
                    )

                # Evaluate project relevance

                with st.spinner(
                    "Evaluating project relevance..."
                ):
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

                # Calculate education score

                education_score = calculate_education_score(
                    st.session_state.job_profile[
                        "education"
                    ],
                    candidate_profile[
                        "education"
                    ]
                )

                # Calculate overall score

                overall_score = calculate_overall_score(
                    required_result["score"],
                    preferred_result["score"],
                    experience_score,
                    education_score,
                    project_relevance_score
                )

                # Save screening results

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

                # Overall candidate score

                st.subheader("🏆 Candidate Score")

                st.metric(
                    "Overall Match Score",
                    f"{overall_score}%"
                )

                # Score breakdown

                st.write("### Score Breakdown")

                st.write(
                    f"Required Skills: "
                    f"**{required_result['score']}%**"
                )

                st.write(
                    f"Preferred Skills: "
                    f"**{preferred_result['score']}%**"
                )

                st.write(
                    f"Experience: "
                    f"**{experience_score}%**"
                )

                st.write(
                    f"Education: "
                    f"**{education_score}%**"
                )

                st.write(
                    f"Project Relevance: "
                    f"**{project_relevance_score}%**"
                )

                # Skill screening

                st.subheader("🎯 Skill Screening")

                st.write(
                    f"**Required Skill Score: "
                    f"{required_result['score']}%**"
                )

                st.write("### Matched Required Skills")

                if required_result["matched_skills"]:
                    st.write(
                        required_result["matched_skills"]
                    )
                else:
                    st.write(
                        "No required skills matched."
                    )

                st.write("### Missing Required Skills")

                if required_result["missing_skills"]:
                    st.write(
                        required_result["missing_skills"]
                    )
                else:
                    st.write(
                        "No required skills are missing."
                    )

                st.write(
                    f"**Preferred Skill Score: "
                    f"{preferred_result['score']}%**"
                )

                st.write("### Matched Preferred Skills")

                if preferred_result["matched"]:
                    st.write(
                        preferred_result["matched"]
                    )
                else:
                    st.write(
                        "No preferred skills matched."
                    )

                st.write("### Missing Preferred Skills")

                if preferred_result["missing"]:
                    st.write(
                        preferred_result["missing"]
                    )
                else:
                    st.write(
                        "No preferred skills are missing."
                    )

                # Requirement evidence

                st.subheader("🧠 Requirement Evidence")

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

                # Project relevance

                st.subheader("📁 Project Relevance")

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