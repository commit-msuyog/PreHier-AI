import json
from groq_helper import ask_groq


def analyze_candidate(resume_text):

    prompt = f"""
You are an AI recruitment assistant.

Analyze the following candidate resume and extract information
that can be used to compare the candidate with a job description.

Return ONLY valid JSON with exactly these fields:

{{
    "name": "",
    "email": "",
    "phone": "",
    "education": [],
    "experience": [],
    "skills": [],
    "projects": [],
    "certifications": [],
    "achievements": []
}}

Rules:
- Do not invent information.
- If something is not mentioned, use an empty string or empty list.
- Keep skills as simple names.
- Keep project descriptions short.
- Keep experience information clear and concise.

Resume:
{resume_text}
"""

    response = ask_groq(prompt)

    try:
        return json.loads(response)

    except json.JSONDecodeError:
        return {
            "error": "Could not parse AI response as JSON",
            "raw_response": response
        }