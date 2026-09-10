from screening.skill_normalizer import normalize_skills


def calculate_skill_match(required_skills, candidate_skills):

    required = normalize_skills(required_skills)
    candidate = normalize_skills(candidate_skills)

    if not required:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": []
        }

    matched = required.intersection(candidate)
    missing = required - candidate

    score = (len(matched) / len(required)) * 100

    return {
        "score": round(score, 2),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing)
    }


def calculate_preferred_skill_match(
    preferred_skills,
    candidate_skills
):

    if not preferred_skills:
        return {
            "score": 100,
            "matched": [],
            "missing": []
        }

    preferred = normalize_skills(preferred_skills)
    candidate = normalize_skills(candidate_skills)

    matched = preferred.intersection(candidate)
    missing = preferred - candidate

    score = (len(matched) / len(preferred)) * 100

    return {
        "score": round(score, 2),
        "matched": sorted(matched),
        "missing": sorted(missing)
    }


def calculate_education_match(
    required_education,
    candidate_education
):

    if not required_education:
        return {
            "score": 100,
            "matched": [],
            "missing": []
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

    if matched:
        score = 100
    else:
        score = 0

    return {
        "score": score,
        "matched": sorted(matched),
        "missing": sorted(missing)
    }