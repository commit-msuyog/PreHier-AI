from skill_normalizer import normalize_skills


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