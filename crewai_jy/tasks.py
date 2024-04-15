from crewai import Task, Agent
from textwrap import dedent

from job_manager import append_event
from models import Finding, NamedUrl, TopicInfo
from utils.logging import logger
from langsmith import wrappers,traceable

@traceable
class AccountResearchTasks():

    def __init__(self, job_id):
        self.job_id = job_id

    def append_event_callback(self, task_output):
        logger.info("Callback called: %s", task_output)
        append_event(self.job_id, task_output.exported_output)
    
    @traceable(name="task.review_research")
    def review_research(self, agent: Agent, target_account: str, topics: list[str], tasks: list[Task]):
        return Task(
            description=dedent(f"""
                You will put together a JSON object on the {target_account} for each of the {topics}. Review the provided URLs, ranking them based 
                on how well they align with the {target_account} and research objective {topics}. Work closely with the researcher to refine this list, 
                recommending specific URLs that are prime candidates for data scraping. Prioritize foundational data (official company publications) 
                then expand to include external analysis and perspectives (industry analysis platforms, business news outlets). Streamline collection 
                of 'findings' by advising on crucial content for JSON inclusion ensuring alignment with research themes. Provide clear directions for 
                extracting relevant information from selected URLs.  
                """),
            agent=agent,
            expected_output=dedent(
                """A JSON object containing the 'target_account', 'topics', and 'findings' each with the source URLs."""),
            callback=self.append_event_callback,
            context=tasks,
            output_json=TopicInfo
        )

    @traceable(name="task.account_research")
    def research_account(self, agent: Agent, target_account: str, topics: list[str]):
        return Task(
            description=dedent(f"""
                You will produce list of 'findings' by performing research on specified {target_account} for each of the {topics}. Identify and list 
                the most relevant URLs for each topic, providing these to the Research Reviewer. Based on feedback, either extract specific 
                text from chosen URLs or gather more sources for evaluation. Compile and return the 'finding' in a JSON object format.
                
                Important:
                - Once you've collected the information, immediately stop searching and promptly report back to the research reviewer for further instructions.
                - Only return the requested information. NOTHING ELSE!
                - Ensure the source URLs for all information is included using the format 'title, URL, year' for each finding.
                - Do not generate fake information. Only return the information you find. Nothing else!
                """),
            agent=agent,
            expected_output="""A JSON object containing the researched information for each topic on the target_account.""",
            callback=self.append_event_callback,
            output_json_list=[NamedUrl, Finding],
            async_execution=True
        )
