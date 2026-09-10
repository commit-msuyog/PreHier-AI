import json

from ai.groq_helper import ask_groq


def evaluate_requirement_evidence(
    required_skills,
    candidate_profile
):

    prompt = f"""
You are an AI recruitment screening assistant.

Evaluate whether the candidate provides evidence for each
required skill.

Required skills:
{json.dumps(required_skills)}

Candidate profile:
{json.dumps(candidate_profile)}

For each required skill, classify the evidence as:

"strong"   → clearly demonstrated through skills, projects,
             experience, or achievements.

"partial"  → related evidence exists, but the requirement
              is not clearly demonstrated.

"none"     → no meaningful evidence found.

Return ONLY valid JSON in this format:

{{
    "requirements": [
        {{
            "skill": "",
            "evidence_level": "",
            "evidence": ""
        }}
    ]
}}

Rules:
- Do not invent evidence.
- Evidence must come from the candidate profile.
- Keep evidence short.
"""

    response = ask_groq(prompt)

    try:
        return json.loads(response)

    except json.JSONDecodeError:

        return {
            "error": "Could not parse AI response",
            "raw_response": response
        }