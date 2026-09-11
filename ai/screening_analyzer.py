import json

from ai.groq_helper import ask_groq, GroqRequestError


def analyze_screening(resume_text, job_profile):

    prompt = f"""
You are an AI recruitment screening assistant.

Analyze this resume against the job profile.

Job Profile:
{json.dumps(job_profile)}

Resume:
{resume_text}

Return ONLY valid JSON in exactly this structure:

{{
    "candidate_profile": {{
        "name": "",
        "email": "",
        "phone": "",
        "education": [],
        "experience": {{
            "years": 0,
            "roles": [],
            "description": ""
        }},
        "skills": [],
        "projects": [],
        "certifications": [],
        "achievements": []
    }},
    "evidence": {{
        "requirements": [
            {{
                "skill": "",
                "evidence_level": "strong|partial|none",
                "evidence": ""
            }}
        ]
    }},
    "projects": {{
        "overall_relevance": "strong|partial|none",
        "projects": [
            {{
                "title": "",
                "relevance": "strong|partial|none",
                "reason": ""
            }}
        ]
    }}
}}

Candidate Profile:
- Extract only information explicitly stated in the resume.
- Use empty strings, empty lists, or 0 when information is unavailable.
- Education, skills, certifications, and achievements must be arrays of strings.
- Projects must contain concise project information.
- Estimate professional experience only when supported by dates.
- Do not count education as work experience.

Requirement Evidence:
- Evaluate every required skill from the job profile.
- strong = clearly demonstrated.
- partial = related evidence exists.
- none = no meaningful evidence.
- Evidence must come only from the resume.
- Keep each evidence statement under 12 words.

Project Relevance:
- Evaluate projects against the job responsibilities and skills.
- strong = directly relevant.
- partial = meaningful but indirect relevance.
- none = little or no relevance.
- Do not assume technologies that are not stated.
- Judge actual project work, not keyword matching alone.
- Keep each project reason under 15 words.

Keep all descriptions concise.
Do not add explanations outside the JSON.
"""

    try:
        response = ask_groq(prompt)
    except GroqRequestError as error:
        return {
            "error": str(error)
        }

    try:
        cleaned_response = response.strip()

        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:].strip()

        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:].strip()

        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3].strip()

        return json.loads(cleaned_response)

    except json.JSONDecodeError:

        return {
            "error": "Could not parse AI response as JSON",
            "raw_response": response
        }