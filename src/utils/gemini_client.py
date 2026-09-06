import os
from dotenv import load_dotenv
from crewai import LLM


load_dotenv()


def get_gemini_llm():
    api_key=os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    return LLM(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.3,
        timeout=5,
        max_retries=1,
    )

