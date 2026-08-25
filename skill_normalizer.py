SKILL_ALIASES = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "sklearn": "scikit-learn",
    "postgres": "postgresql",
    "js": "javascript",
    "ts": "typescript",
    "node": "node.js",
    "nodejs": "node.js",
}


def normalize_skill(skill):
    skill = skill.strip().lower()

    return SKILL_ALIASES.get(skill, skill)


def normalize_skills(skills):
    return {
        normalize_skill(skill)
        for skill in skills
    }