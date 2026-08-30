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

Evaluate how relevant the candidate's projects are to the job.

Job Profile:
{json.dumps(job_profile)}

Candidate Projects:
{json.dumps(projects)}

For each project, classify relevance as:

"strong"   → project directly demonstrates skills or work
             relevant to the job.

"partial"  → project has some relevant concepts but does not
             directly demonstrate the job requirements.

"none"     → project has little or no relevance.

Return ONLY valid JSON:

{{
    "overall_relevance": "",
    "projects": [
        {{
            "title": "",
            "relevance": "",
            "reason": ""
        }}
    ]
}}

Rules:
- Do not invent project details.
- Use only information provided in the candidate projects.
- Keep reasons short.
- Consider the required and preferred skills.
- Consider the job responsibilities.
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