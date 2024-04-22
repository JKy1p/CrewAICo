from datetime import datetime
from typing import Callable
from langchain_openai import ChatOpenAI
from agents import AccountResearchAgents
from job_manager import append_event
from tasks import AccountResearchTasks
from crewai import Task, Crew
from langsmith import traceable
from utils.logging import debug_process_inputs

class AccountResearchCrew:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.crew = None
        self.tasks = list[Task]
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    @traceable(name="setup crew", run_type="chain", process_inputs=debug_process_inputs)    
    def setup_crew(self, target_account: str, topics: list[str]):
        agents = AccountResearchAgents()
        tasks = AccountResearchTasks(
            job_id=self.job_id)

        report_writer = agents.report_writer(target_account, topics)
        research_manager = agents.research_manager(target_account, topics)
        strategy_researcher = agents.strategy_researcher() 
        account_researcher = agents.account_researcher()

        research_account_tasks = [
            tasks.research_account(account_researcher, topic, target_account)
            for topic in topics
        ]
        
        research_strategy_tasks = [
            tasks.research_strategy(strategy_researcher, target_account, topic, research_account_tasks)  
            for topic in topics
        ]

        manage_research_tasks = [
            tasks.manage_research(research_manager, target_account, topic, research_account_tasks + research_strategy_tasks)  
            for topic in topics
        ]
        
        write_report_task = tasks.write_report(
            report_writer, target_account, topics, manage_research_tasks)
        
        
        self.crew = Crew(
            agents=[report_writer, research_manager, account_researcher],
            tasks=[*research_account_tasks, *research_strategy_tasks, *manage_research_tasks, write_report_task],
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
