from pypdf import PdfReader

from ai.candidate_analyzer import analyze_candidate

from screening.matching_engine import (
    calculate_skill_match,
    calculate_preferred_skill_match
)

from screening.scoring_engine import (
    calculate_experience_score,
    calculate_education_score,
    calculate_overall_score,
    relevance_to_score
)

from screening.evidence_matcher import evaluate_requirement_evidence
from screening.project_matcher import evaluate_project_relevance


def extract_resume_text(resume):

    reader = PdfReader(resume)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text + "\n"

    return resume_text


def screen_resume(resume, job_profile):

    resume_text = extract_resume_text(resume)

    candidate_profile = analyze_candidate(
        resume_text
    )

    required_experience = (
        job_profile["experience_required"]
    )

    required_years = required_experience.get(
        "years",
        0
    )

    candidate_years = (
        candidate_profile["experience"].get(
            "years",
            0
        )
    )

    experience_score = calculate_experience_score(
        required_years,
        candidate_years
    )

    required_result = calculate_skill_match(
        job_profile["required_skills"],
        candidate_profile["skills"]
    )

    preferred_result = calculate_preferred_skill_match(
        job_profile["preferred_skills"],
        candidate_profile["skills"]
    )

    evidence_result = evaluate_requirement_evidence(
        job_profile["required_skills"],
        candidate_profile
    )

    project_result = evaluate_project_relevance(
        job_profile,
        candidate_profile["projects"]
    )

    project_relevance_score = relevance_to_score(
        project_result.get(
            "overall_relevance",
            "none"
        )
    )

    education_score = calculate_education_score(
        job_profile["education"],
        candidate_profile["education"]
    )

    overall_score = calculate_overall_score(
        required_result["score"],
        preferred_result["score"],
        experience_score,
        education_score,
        project_relevance_score
    )

    match_result = {
        "required_skills": required_result,
        "preferred_skills": preferred_result,
        "experience_score": experience_score,
        "education_score": education_score,
        "project_relevance_score": project_relevance_score,
        "overall_score": overall_score,
        "evidence": evidence_result,
        "projects": project_result
    }

    return candidate_profile, match_result