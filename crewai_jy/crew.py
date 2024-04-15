from datetime import datetime
from typing import Callable
from langchain_openai import ChatOpenAI
from agents import AccountResearchAgents
from job_manager import append_event
from tasks import AccountResearchTasks
from crewai import Crew
from langsmith import traceable

@traceable(name="crew.account_research")
class AccountResearchCrew:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.crew = None
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def setup_crew(self, target_account: str, topics: list[str]):
        agents = AccountResearchAgents()
        tasks = AccountResearchTasks(
            job_id=self.job_id)

        research_reviewer = agents.research_reviewer(
            target_account, topics)
        account_researcher = agents.account_researcher()

        account_research_tasks = [
            tasks.research_account(account_researcher, target_account, topics)
            for account in target_account
        ]

        review_research_task = tasks.review_research(
            research_reviewer, target_account, topics, account_research_tasks)

        self.crew = Crew(
            agents=[research_reviewer, account_researcher],
            tasks=[*account_research_tasks, review_research_task],
            verbose=2,
        )

    def kickoff(self):
        if not self.crew:
            append_event(self.job_id, "Crew not set up")
            return "Crew not set up"

        append_event(self.job_id, "Task Started")
        try:
            results = self.crew.kickoff()
            append_event(self.job_id, "Task Complete")
            return results
        except Exception as e:
            append_event(self.job_id, f"An error occurred: {e}")
            return str(e)
