import json
from ai.groq_helper import ask_groq


def analyze_job_description(job_description):

    prompt = f"""
You are an AI recruitment assistant.

Analyze the following job description and extract the important
requirements for screening candidates.

Return ONLY valid JSON.

Use exactly these fields:

{{
    "job_title": "",
    "required_skills": [],
    "preferred_skills": [],
    "experience_required": {{
        "years": 0,
        "description": ""
    }},
    "education": [],
    "responsibilities": []
}}

Rules:
- Do not invent information.
- If something is not mentioned, use an empty string or empty list.
- Keep skills as simple names.
- Keep responsibilities short and clear.
- Extract the minimum required years of experience if mentioned.
- If no years are mentioned, use 0.
- Put other experience requirements in description.

Job Description:
{job_description}
"""

    response = ask_groq(prompt)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "error": "Could not parse AI response as JSON",
            "raw_response": response
        }