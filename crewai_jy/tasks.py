from crewai import Task, Agent
from textwrap import dedent
from job_manager import append_event
from models import Source, SourceInfo, FindingInfo, TopicInfo
from utils.logging import logger, debug_process_inputs
from typing import List
from langsmith import wrappers, traceable



@traceable
class AccountResearchTasks():

    def __init__(self, job_id):
        self.job_id = job_id
        # self.factory = DefaultFactory()
        # source= self.factory.do_source()
        # source_info = self.factory.do_source_info()
        # finding_info = self.factory.do_finding_info()
        # topic_info = self.factory.do_topic_info()
        self.source = Source()
        self.source_info = SourceInfo()
        self.finding_info = FindingInfo()
        self.topic_info = TopicInfo()


    def append_event_callback(self, task_output):
        logger.info("Callback called: %s", task_output)
        append_event(self.job_id, task_output.exported_output)
    
    @traceable(name="review research", run_type="prompt", process_inputs=debug_process_inputs)    
    def review_research(self, agent: Agent, target_account: str, topics: list[str], tasks: list[Task]):
        return Task(            
            description=dedent(f"""
                Review and refine a comprehensive 'TopicInfo' JSON object for the {target_account} for each specified of the {topics}. 
                Evaluate sourceinfo and highlights collected by the Account Researcher to ensure alignment with strategic research objectives.
                
                Action Items:
                - Prioritize recent and credible sources such as official company websites, annual reports, and relevant press releases.
                - Suggest secondary sources like industry analyses and business news for broader context.
                - Rank all sources based on their relevance to the research objectives.
                - Provide clear, actionable feedback to refine the researcher's approach.
                """),
            agent=agent,
            expected_output=dedent(
                """A 'TopicInfo' JSON object compiled as a list of 'Finding' JSON objects, each meticulously evaluated for relevance 
                and accuracy."""),
            callback=self.append_event_callback,
            context=tasks,
            output_json=[self.topic_info],
        )

    @traceable(name="research account", run_type="retriever", process_inputs=debug_process_inputs)    
    def research_account(self, agent: Agent, target_account: str, topics: list[str]):
        return Task(
            description=dedent(f"""
                Conduct in-depth research and create detailed 'finding' JSON objects for the {target_account} and each of the 
                specified research {topics}. The task is segmented into three phases: Initial Research, Follow-up Based on Feedback, 
                and Compilation of 'Finding' JSON Objects.
                
                Action Items:
                1. Initial Research:
                - Identify and gather 'sourceinfo' with relevant information to the research topics.
                - Submit for preliminary review.
                2. Follow-up Based on Feedback:
                - Enhance data depth based on feedback adjusting your research approach 
                - Collect more targeted data with enriched data details and submit for review.
                3. Compilation of 'Finding' JSON Objects:
                - Compile the final findings into comprehensive JSON objects.
                - 'Finding' JSON object includes essential elements such as title, URL, publication year, and 3-5 snippets.

                Important Guidelines:
                - Do not fabricate information; only include data found in the URLs.
                - Prioritize recent information by limiting sources to those from the last 4 years.
                """),
            agent=agent,
            expected_output="A 'Finding' JSON object",
            callback=self.append_event_callback,
            output_json=[self.source, self.source_info, self.finding_info], 
            async_execution=True
        )


    # @traceable(name="review research", run_type="prompt", process_inputs=debug_process_inputs)    
    # def review_research(self, agent: Agent, target_account: str, topics: list[str], feedback_tasks: list[Task]):
    #     return Task(
    #         description=dedent(f"""
    #             You will put together a 'TopicInfo' JSON object on the {target_account} for each of the {topics}. Your role is to scrutinize the list 
    #             of URLs submitted by the Account Researcher based on how well they align with the {target_account} and research objective {topics}. 
    #             Provide structured feedback in your task assignment that helps the researcher refine their approach:
                
    #             - Prioritize recent URLs from official company websites, annual reports, and press releases that provide foundational data
    #             - Recommend expansion into secondary sources such as industry analyses and business news that offer broader perspectives.
    #             - Rank the URLs based on their alignment with the research objectives and {target_account}'s specifics.
    #             - Advise on key content within these URLs to be scraped or further analyzed.
                
    #             Provide structured and actionable instructions so the researcher is clear on subsequent steps, whether it involves deeper data 
    #             extraction or additional sourcing.            

    #             """),
    #         agent=agent,
    #         expected_output=dedent(
    #             """A JSON object containing the 'target_account', 'topics', and 'findings' each with the source URLs."""),
    #         callback=self.append_event_callback,
    #         context=feedback_tasks,
    #         output_json=TopicInfo
    #     )

    # @traceable(name="research account", run_type="retriever", process_inputs=debug_process_inputs)    
    # def research_account(self, agent: Agent, target_account: str, topics: list[str]):
    #     return Task(
    #         description=dedent(f"""
    #         Your primary objective is to create multiple 'finding' JSON objects for {target_account}, each corresponding to the specified {topics}. 
    #         Begin by identifying and compiling a list of the most relevant URLs that pertain to each topic. Submit these URLs in a JSON format to 
    #         the Research Reviewer for initial feedback.
            
    #         - If the feedback indicates a need for more detailed information, use tools like 'get_content' to extract specific text from the provided URLs.
    #         - If additional sources are required, gather more URLs with the 'search' tool or use 'find_similar' to locate related content.
    #         - Compile and return the finding in a JSON object format, ensuring each finding includes 'title, URL, year, list of snippets'.

    #         Important:
    #         - Do not make up information. Only return the information you find. Nothing else!
    #         - Prioritize recent information by limiting source URLs to include only those from the last 4 years.
    #         - Cease further searching after the initial submission and do not continue with any actions until you receive feedback from the Research Reviewer.
    #         """),
    #         agent=agent,
    #         expected_output="A 'Finding' JSON object, compiled from a list of relevant URLs for each topic on the target_account.",
    #         callback=self.append_event_callback,
    #         output_json_list=[NamedUrlList, Finding],
    #         async_execution=True
    #     )

