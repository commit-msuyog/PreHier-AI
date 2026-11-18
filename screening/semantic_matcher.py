
from functools import lru_cache

from sentence_transformers import SentenceTransformer, util

from screening.skill_normalizer import normalize_skills
from screening.skill_relationships import SKILL_RELATIONSHIPS


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Conservative experimental threshold for embedding-based matches.
DEFAULT_SIMILARITY_THRESHOLD = 0.65

# Embedding-only matches receive less credit than curated relationships.
SEMANTIC_MATCH_CREDIT = 0.25


SKILL_CONTEXT = {
    "machine learning": (
        "Field of artificial intelligence involving training "
        "statistical models to learn patterns from data."
    ),
    "scikit-learn": (
        "Python library for machine learning, classification, "
        "regression, clustering and model evaluation."
    ),
    "deep learning": (
        "Machine learning approach using multi-layer neural "
        "networks to learn representations from data."
    ),
    "tensorflow": (
        "Deep learning framework used to build and train "
        "neural networks and machine learning models."
    ),
    "pytorch": (
        "Deep learning framework used for tensor computation "
        "and neural network training."
    ),
    "rest api": (
        "API design using HTTP methods and resource-based "
        "communication between software applications."
    ),
    "fastapi": (
        "Python web framework for developing HTTP APIs "
        "and REST API services."
    ),
    "computer vision": (
        "Artificial intelligence field involving image "
        "processing, visual recognition and video analysis."
    ),
    "opencv": (
        "Computer vision library for image processing, "
        "video analysis and visual object detection."
    ),
}


@lru_cache(maxsize=1)
def load_embedding_model():
    """Load the embedding model once and reuse it."""
    return SentenceTransformer(MODEL_NAME)


def get_skill_description(skill):
    """Return contextual information for a skill."""
    return SKILL_CONTEXT.get(
        skill,
        f"Technical skill, software technology or tool: {skill}."
    )


def calculate_semantic_skill_match(
    required_skills,
    candidate_skills,
    threshold=DEFAULT_SIMILARITY_THRESHOLD,
):
    """
    Hybrid skill matching:

    1. Exact normalized matches.
    2. Curated technical relationships.
    3. Contextual embedding similarity.
    4. Missing skills.

    Each candidate skill can be used only once.
    """

    required = sorted(normalize_skills(required_skills))
    candidate = sorted(normalize_skills(candidate_skills))

    if not required:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "exact_matches": [],
            "related_matches": [],
            "semantic_matches": [],
            "match_details": [],
        }

    # --------------------------------------------------
    # 1. Exact matching
    # --------------------------------------------------

    exact_matches = sorted(set(required) & set(candidate))

    unmatched_required = set(required) - set(exact_matches)
    unmatched_candidate = set(candidate) - set(exact_matches)

    related_matches = []

    # --------------------------------------------------
    # 2. Curated relationship matching
    # --------------------------------------------------

    possible_related_matches = []

    for required_skill in unmatched_required:

        relationships = SKILL_RELATIONSHIPS.get(
            required_skill, {}
        )

        for candidate_skill, credit in relationships.items():

            if candidate_skill not in unmatched_candidate:
                continue

            possible_related_matches.append({
                "required_skill": required_skill,
                "matched_skill": candidate_skill,
                "match_type": "curated_related",
                "similarity": None,
                "credit": float(credit),
            })

    possible_related_matches.sort(
        key=lambda item: item["credit"],
        reverse=True,
    )

    used_required = set()
    used_candidate = set()

    for match in possible_related_matches:

        required_skill = match["required_skill"]
        candidate_skill = match["matched_skill"]

        if required_skill in used_required:
            continue

        if candidate_skill in used_candidate:
            continue

        related_matches.append(match)

        used_required.add(required_skill)
        used_candidate.add(candidate_skill)

    unmatched_required -= used_required
    unmatched_candidate -= used_candidate

    # --------------------------------------------------
    # 3. Contextual semantic matching
    # --------------------------------------------------

    semantic_matches = []

    if unmatched_required and unmatched_candidate:

        remaining_required = sorted(unmatched_required)
        remaining_candidate = sorted(unmatched_candidate)

        model = load_embedding_model()

        required_descriptions = [
            get_skill_description(skill)
            for skill in remaining_required
        ]

        candidate_descriptions = [
            get_skill_description(skill)
            for skill in remaining_candidate
        ]

        required_embeddings = model.encode(
            required_descriptions,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        candidate_embeddings = model.encode(
            candidate_descriptions,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        similarities = util.cos_sim(
            required_embeddings,
            candidate_embeddings,
        )

        possible_semantic_matches = []

        for i, required_skill in enumerate(remaining_required):
            for j, candidate_skill in enumerate(remaining_candidate):

                similarity = float(similarities[i][j].item())

                if similarity >= threshold:
                    possible_semantic_matches.append({
                        "required_skill": required_skill,
                        "matched_skill": candidate_skill,
                        "match_type": "semantic",
                        "similarity": round(similarity, 4),
                        "credit": SEMANTIC_MATCH_CREDIT,
                    })

        possible_semantic_matches.sort(
            key=lambda item: item["similarity"],
            reverse=True,
        )

        used_required = set()
        used_candidate = set()

        for match in possible_semantic_matches:

            required_skill = match["required_skill"]
            candidate_skill = match["matched_skill"]

            if required_skill in used_required:
                continue

            if candidate_skill in used_candidate:
                continue

            semantic_matches.append(match)

            used_required.add(required_skill)
            used_candidate.add(candidate_skill)

        unmatched_required -= used_required

    # --------------------------------------------------
    # 4. Missing skills
    # --------------------------------------------------

    missing_skills = sorted(unmatched_required)

    # --------------------------------------------------
    # 5. Weighted score
    # --------------------------------------------------

    exact_credit = len(exact_matches)

    related_credit = sum(
        match["credit"] for match in related_matches
    )

    semantic_credit = sum(
        match["credit"] for match in semantic_matches
    )

    total_credit = (
        exact_credit + related_credit + semantic_credit
    )

    score = (total_credit / len(required)) * 100

    # --------------------------------------------------
    # 6. Explainable results
    # --------------------------------------------------

    all_matches = (
        related_matches + semantic_matches
    )

    matched_skills = sorted(
        set(exact_matches)
        | {
            match["required_skill"]
            for match in all_matches
        }
    )

    match_details = [
        {
            "required_skill": skill,
            "matched_skill": skill,
            "match_type": "exact",
            "credit": 1.0,
        }
        for skill in exact_matches
    ] + all_matches

    return {
        "score": round(score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "exact_matches": exact_matches,
        "related_matches": related_matches,
        "semantic_matches": semantic_matches,
        "match_details": match_details,
    }
