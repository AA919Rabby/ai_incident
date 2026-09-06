from crewai import Agent
from src.utils.gemini_client import get_gemini_llm


def create_analyst():
    return Agent(
        role="Senior city data analyst",
        goal="Analyze incoming incident data and ML predictions to understand the full  scope of the emergency.",
        backstory="You are an expert in urban planning and emergency data analysis. You synthesize raw ML data into human-readable insights.",
        verbose=True,
        allow_delegation=False,
        llm=get_gemini_llm()
    )