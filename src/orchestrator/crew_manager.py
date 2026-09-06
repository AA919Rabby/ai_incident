from crewai import Crew, Task, Process
from src.agents.analyst_agent import create_analyst
from src.agents.response_agent import create_responder
from src.agents.notification_agent import create_notifier
from src.models.tensorflow_model import IncidentClassifierTF
from src.models.pytorch_model import IncidentForecasterPT

class IncidentOrchestrator:
    def __init__(self):
        self.tf_model = IncidentClassifierTF()
        self.pt_model = IncidentForecasterPT()

    def process_incident(self, description: str):
        # 1. Create FRESH Agents
        analyst = create_analyst()
        responder = create_responder()
        notifier = create_notifier()

        # Prevent infinite loops
        analyst.max_iter = 2
        responder.max_iter = 2
        notifier.max_iter = 2

        # 2. TASK 1: The Analyst gathers the "Sources" and analyzes the situation
        analysis_task = Task(
            description=f"User request: '{description}'.\nINSTRUCTION: You do not have internet access. You must SIMULATE checking local news APIs and Traffic Cameras. Write a detailed analysis of the situation. You MUST include a section titled 'SOURCES USED:' detailing where you simulated getting this information from.",
            expected_output="A situation report including a 'SOURCES USED' section explaining where the data came from.",
            agent=analyst
        )

        # 3. TASK 2: The Responder creates the Plan
        response_task = Task(
            description="Based on the Analyst's report, provide 3 bullet points on how authorities or citizens should respond.",
            expected_output="3 bullet points of actionable advice.",
            agent=responder
        )

        # 4. TASK 3: Notifier tweets
        notification_task = Task(
            description="Draft a 1-sentence public safety tweet based on the plan.",
            expected_output="A 1-sentence tweet.",
            agent=notifier
        )

        # 5. Execute
        crew = Crew(
            agents=[analyst, responder, notifier],
            tasks=[analysis_task, response_task, notification_task],
            process=Process.sequential,
            verbose=True
        )

        # Get final plan
        final_result = crew.kickoff()

        # Get the source & reasoning directly from the Analyst Agent's task
        analyst_source_report = str(analysis_task.output)

        # Return both cleanly to the UI
        return {
            "source_info": analyst_source_report,  # This goes to Column 2 (The Source)
            "final_action_plan": str(final_result) # This goes to Column 1 (The Result)
        }