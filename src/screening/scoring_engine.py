def calculate_skill_score(required_skills, candidate_skills):

    required = {
        skill.strip().lower()
        for skill in required_skills
    }

    candidate = {
        skill.strip().lower()
        for skill in candidate_skills
    }

    if not required:
        return 0

    matched = required.intersection(candidate)

    return round(
        (len(matched) / len(required)) * 100,
        2
    )


def calculate_preferred_score(preferred_skills, candidate_skills):

    preferred = {
        skill.strip().lower()
        for skill in preferred_skills
    }

    candidate = {
        skill.strip().lower()
        for skill in candidate_skills
    }

    if not preferred:
        return 100

    matched = preferred.intersection(candidate)

    return round(
        (len(matched) / len(preferred)) * 100,
        2
    )


def calculate_overall_score(
    required_skill_score,
    preferred_skill_score,
    experience_score,
    education_score
):

    score = (
        required_skill_score * 0.50
        + preferred_skill_score * 0.15
        + experience_score * 0.20
        + education_score * 0.15
    )

    return round(score, 2)