def calculate_experience_score(required_years, candidate_years):

    if required_years <= 0:
        return 100

    if candidate_years >= required_years:
        return 100

    score = (candidate_years / required_years) * 100

    return round(score, 2)