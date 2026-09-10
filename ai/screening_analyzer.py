import json

from ai.groq_helper import ask_groq


def analyze_screening(resume_text, job_profile):

    prompt = f"""
You are an AI recruitment screening assistant.

Analyze the candidate resume against the provided job profile.

Job Profile:
{json.dumps(job_profile)}

Resume:
{resume_text}

Return ONLY valid JSON with exactly these fields:

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
        "requirements": []
    }},
    "projects": {{
        "overall_relevance": "strong|partial|none",
        "projects": []
    }}
}}

Candidate Profile Rules:
- Do not invent information.
- If information is not mentioned, use an empty string, empty list, or 0.
- Education MUST be an array of strings.
- Skills MUST be an array of strings.
- Certifications MUST be an array of strings.
- Achievements MUST be an array of strings.
- Keep project descriptions short.
- Estimate total professional work experience only when the dates support it.
- Do not count education as work experience.
- If experience cannot be determined, use 0.
- Include relevant job roles in roles.
- Keep relevant work details in description.

Requirement Evidence Rules:
Evaluate each required skill from the job profile.

Use:
"strong" → clearly demonstrated through skills, projects,
             experience, or achievements.

"partial" → related evidence exists, but the requirement
             is not clearly demonstrated.

"none" → no meaningful evidence found.

For each requirement return:

{{
    "skill": "",
    "evidence_level": "strong|partial|none",
    "evidence": ""
}}

- Evidence must come only from the candidate resume.
- Do not invent evidence.
- Keep evidence short and factual.

Project Relevance Rules:
Evaluate each candidate project against the job profile.

Consider:
1. Similarity between the project's actual work and job responsibilities.
2. Concepts related to required skills.
3. Concepts related to preferred skills.
4. Technical domain and type of problem solved.
5. Demonstrated application of relevant knowledge.

Do NOT require the project description to explicitly mention
every technology in the job description.

Do NOT assume a technology was used unless it is explicitly stated.

Classify each project as:

"strong" → directly demonstrates work or concepts highly relevant
            to the job.

"partial" → meaningful overlap exists but does not directly
             demonstrate the main requirements.

"none" → little or no meaningful relationship to the job.

For each project return:

{{
    "title": "",
    "relevance": "strong|partial|none",
    "reason": ""
}}

- Do not invent project details.
- Use only information provided in the resume.
- Keep reasons concise and factual.
- Judge project relevance based on actual work, not keyword
  matching alone.

The "overall_relevance" value must be:
"strong", "partial", or "none".
"""

    response = ask_groq(prompt)

    try:
        cleaned_response = response.strip()

        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response.replace(
                "```json",
                "",
                1
            ).replace(
                "```",
                "",
                1
            ).strip()

        return json.loads(cleaned_response)

    except json.JSONDecodeError:

        return {
            "error": "Could not parse AI response as JSON",
            "raw_response": response
        }