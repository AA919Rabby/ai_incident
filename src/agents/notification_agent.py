from crewai import Agent
from src.utils.gemini_client import get_gemini_llm

def create_notifier():
    return Agent(
        role='Public Information Officer',
        goal='Draft public warnings and internal government briefings regarding the incident.',
        backstory="You are the voice of the city. You communicate clearly, preventing panic while ensuring public safety.",
        verbose=True,
        allow_delegation=False,
        llm=get_gemini_llm()
    )