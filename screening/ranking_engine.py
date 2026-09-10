def rank_candidates(match_results):
    ranked_candidates = []

    for candidate_name, result in match_results.items():
        ranked_candidates.append({
            "candidate": candidate_name,
            "score": result.get("overall_score", 0)
        })

    ranked_candidates.sort(
        key=lambda candidate: candidate["score"],
        reverse=True
    )

    for rank, candidate in enumerate(
        ranked_candidates,
        start=1
    ):
        candidate["rank"] = rank

    return ranked_candidates