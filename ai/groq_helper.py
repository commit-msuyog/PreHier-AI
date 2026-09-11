import os

from dotenv import load_dotenv
from groq import Groq, GroqError

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class GroqRequestError(Exception):
    """Raised when the Groq API call itself fails (network, auth, rate limit).

    Callers should catch this alongside json.JSONDecodeError so that any
    AI failure surfaces as a recruiter-friendly message instead of an
    unhandled traceback.
    """


def ask_groq(prompt):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={
                "type": "json_object"
            },
            max_tokens=3000
        )

        return response.choices[0].message.content

    except GroqError as error:
        raise GroqRequestError(
            f"The AI service could not complete this request ({error})."
        ) from error

    except Exception as error:
        raise GroqRequestError(
            f"Unexpected error while contacting the AI service ({error})."
        ) from error
