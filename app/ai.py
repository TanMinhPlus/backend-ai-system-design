import os
from functools import lru_cache

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


@lru_cache(maxsize=1)
def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key.startswith("your_"):
        raise RuntimeError("GROQ_API_KEY is not configured")
    return Groq(api_key=api_key)


def run_chat(prompt: str) -> str:
    response = get_groq_client().chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""


def summarize_note(content: str) -> str:
    try:
        return run_chat(
            "Summarize the following note concisely in English. "
            "Focus on the actionable ideas and system design concepts:\n\n"
            f"{content}"
        )
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"AI summarize failed: {str(e)}")


def ask_about_note(content: str, question: str) -> str:
    try:
        return run_chat(
            "Answer the question using only the note content below. "
            "If the note does not contain the answer, say that clearly.\n\n"
            f"Note:\n{content}\n\nQuestion: {question}"
        )
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"AI Q&A failed: {str(e)}")
