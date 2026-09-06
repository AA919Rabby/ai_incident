from crewai import Agent
from src.utils.gemini_client import get_gemini_llm

def create_responder():
    return Agent(
        role='Emergency Response Coordinator',
        goal='Develop a concrete, step-by-step action plan to resolve the incident based on the Analyst report.',
        backstory="A veteran first responder commander. You know exactly which units to dispatch and how to contain city crises.",
        verbose=True,
        allow_delegation=False,
        llm=get_gemini_llm()
    )