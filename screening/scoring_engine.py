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

def relevance_to_score(relevance):

    relevance = relevance.lower().strip()

    mapping = {
        "strong": 100,
        "partial": 50,
        "none": 0
    }

    return mapping.get(relevance, 0)

def calculate_experience_score(
    required_years,
    candidate_years
):

    required_years = float(required_years or 0)
    candidate_years = float(candidate_years or 0)

    if required_years <= 0:
        return 100

    if candidate_years >= required_years:
        return 100

    score = (
        candidate_years / required_years
    ) * 100

    return round(score, 2)

def calculate_education_score(
    required_education,
    candidate_education
):

    if not required_education:
        return 100

    required = " ".join(
        education.lower()
        for education in required_education
    )

    candidate = " ".join(
        education.lower()
        for education in candidate_education
    )

    # Degree-level matching
    degree_levels = [
        ("phd", 4),
        ("doctorate", 4),
        ("master", 3),
        ("m.tech", 3),
        ("mca", 3),
        ("bachelor", 2),
        ("b.tech", 2),
        ("b.e", 2),
        ("bca", 2),
        ("diploma", 1)
    ]

    required_level = 0
    candidate_level = 0

    for keyword, level in degree_levels:
        if keyword in required:
            required_level = max(required_level, level)

        if keyword in candidate:
            candidate_level = max(candidate_level, level)

    if candidate_level >= required_level:
        return 100

    if candidate_level > 0 and required_level > 0:
        return round(
            (candidate_level / required_level) * 100,
            2
        )

    return 0


def calculate_overall_score(
    required_skill_score,
    preferred_skill_score,
    experience_score,
    education_score,
    project_relevance_score
):

    score = (
        required_skill_score * 0.40
        + preferred_skill_score * 0.15
        + experience_score * 0.15
        + education_score * 0.10
        + project_relevance_score * 0.20
    )

    return round(score, 2)