def compare_candidates(
    ranked_candidates,
    candidate_results
):
    comparison = []

    for candidate in ranked_candidates:
        candidate_name = candidate["candidate"]

        result = candidate_results.get(
            candidate_name,
            {}
        )

        comparison.append({
            "candidate": candidate_name,
            "overall_score": result.get(
                "overall_score",
                0
            ),
            "required_skills": result.get(
                "required_skills",
                {}
            ).get("score", 0),
            "preferred_skills": result.get(
                "preferred_skills",
                {}
            ).get("score", 0),
            "experience": result.get(
                "experience_score",
                0
            ),
            "education": result.get(
                "education_score",
                0
            ),
            "project_relevance": result.get(
                "project_relevance_score",
                0
            )
        })

    return comparison