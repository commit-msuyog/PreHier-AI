from screening.skill_normalizer import normalize_skills
from screening.semantic_matcher import calculate_semantic_skill_match


def calculate_skill_match(required_skills, candidate_skills):

    result = calculate_semantic_skill_match(
        required_skills=required_skills,
        candidate_skills=candidate_skills,
    )

    return {
        "score": result["score"],
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "exact_matches": result["exact_matches"],
        "related_matches": result["related_matches"],
        "semantic_matches": result["semantic_matches"],
        "match_details": result["match_details"],
    }


def calculate_preferred_skill_match(
    preferred_skills,
    candidate_skills,
):

    if not preferred_skills:
        return {
            "score": 100,
            "matched": [],
            "missing": [],
            "exact_matches": [],
            "related_matches": [],
            "semantic_matches": [],
            "match_details": [],
        }

    result = calculate_semantic_skill_match(
        required_skills=preferred_skills,
        candidate_skills=candidate_skills,
    )

    return {
        "score": result["score"],
        "matched": result["matched_skills"],
        "missing": result["missing_skills"],
        "exact_matches": result["exact_matches"],
        "related_matches": result["related_matches"],
        "semantic_matches": result["semantic_matches"],
        "match_details": result["match_details"],
    }


def calculate_education_match(
    required_education,
    candidate_education,
):
    """
    Calculate education match using exact matching.
    """

    if not required_education:
        return {
            "score": 100,
            "matched": [],
            "missing": [],
        }

    required = {
        education.strip().lower()
        for education in required_education
    }

    candidate = {
        education.strip().lower()
        for education in candidate_education
    }

    matched = required.intersection(candidate)
    missing = required - candidate

    score = 100 if matched else 0

    return {
        "score": score,
        "matched": sorted(matched),
        "missing": sorted(missing),
    }