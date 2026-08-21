def calculate_skill_match(required_skills, candidate_skills):

    required = {
        skill.strip().lower()
        for skill in required_skills
    }

    candidate = {
        skill.strip().lower()
        for skill in candidate_skills
    }

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