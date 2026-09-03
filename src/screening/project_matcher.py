import json

from src.ai.groq_helper import ask_groq


def evaluate_project_relevance(
    job_profile,
    projects
):
    if not projects:
        return {
            "overall_relevance": "none",
            "projects": []
        }

    prompt = f"""
You are an AI recruitment screening assistant.

Evaluate how relevant each candidate project is to the job.

Job Profile:
{json.dumps(job_profile)}

Candidate Projects:
{json.dumps(projects)}

Evaluate project relevance based primarily on:

1. Similarity between the project's actual work and the job responsibilities.
2. Whether the project demonstrates concepts related to the required skills.
3. Whether the project demonstrates concepts related to the preferred skills.
4. The technical domain and type of problem solved.
5. The candidate's demonstrated application of relevant knowledge.

IMPORTANT:
Do NOT require a project description to explicitly mention every
technology listed in the job description.

For example, if a project demonstrates machine learning model
development and the job requires machine learning, the project can
still be highly relevant even if the project description does not
explicitly mention Pandas, NumPy, or Scikit-learn.

Do NOT assume that a technology was used if it is not stated.
However, judge the overall relevance of the project based on the
work that is explicitly described.

Classify each project as:

"strong" → The project directly demonstrates work or concepts that
            are highly relevant to the job.

"partial" → The project has meaningful overlap with the job but does
             not directly demonstrate the main requirements.

"none" → The project has little or no meaningful relationship to
         the job.

Return ONLY valid JSON:

{{
    "overall_relevance": "strong|partial|none",
    "projects": [
        {{
            "title": "",
            "relevance": "strong|partial|none",
            "reason": ""
        }}
    ]
}}

Rules:
- Do not invent project details.
- Use only information provided in the candidate projects and job profile.
- Do not claim a specific technology was used unless it is explicitly stated.
- Judge overall project relevance, not keyword matching alone.
- Consider job responsibilities as well as skills.
- Keep reasons concise and factual.
"""

    response = ask_groq(prompt)

    try:
        cleaned_response = response.strip()

        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response.replace(
                "```json", "", 1
            ).replace(
                "```", "", 1
            ).strip()

        return json.loads(cleaned_response)

    except json.JSONDecodeError:
        return {
            "error": "Could not parse project relevance response",
            "raw_response": response
        }