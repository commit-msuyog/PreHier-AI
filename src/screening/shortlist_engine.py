def create_shortlist(
    ranked_candidates,
    selected_candidates
):
    shortlist = []

    for candidate in ranked_candidates:
        if candidate["candidate"] in selected_candidates:
            shortlist.append(candidate)

    return shortlist