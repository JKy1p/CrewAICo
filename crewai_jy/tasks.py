from crewai import Task, Agent
from textwrap import dedent
from job_manager import append_event
from models import SubTopic, TopicInfo, AccountInfo
from utils.logging import logger, debug_process_inputs
from langsmith import wrappers, traceable



@traceable
class AccountResearchTasks():
    def __init__(self, job_id: str):
        self.job_id = job_id

    def append_event_callback(self, task_output):
        logger.info("Callback called: %s", task_output)
        append_event(self.job_id, task_output.exported_output)
        
        
    # @traceable(name="review research", run_type="prompt", process_inputs=debug_process_inputs)    
    def write_report(self, agent: Agent, target_account: str, topics: list[str], tasks: list[Task]):
        return Task(            
            agent=agent,
            description=dedent(f"""
                Create a comprehensive and structured report that integrates all collected information on {target_account} with findings 
                and insights for each of the {topics}.                
                
                Action Items:
                - Set clear objectives for each section of the report at the AccountInfo level, ensuring comprehensive coverage of all topics.
                - Ensure each topic section includes 3-5 detailed findings with comprehensive descriptions and sources.
                - Provide feedback if additional information is needed, guiding the research team to fill any gaps in data or analysis.
                - Review feedback from all research phases to ensure the report's completeness and accuracy.
                - Outline strategic implications of the research with supporting sources and insights.
                
                Guidelines:
                - All factual data must include a source title, URL, and year published.
                - Use clear, concise language to ensure readability and ease of understanding.
                """),
            expected_output=dedent(
                """A comprehensive and detailed report encapsulated in the AccountInfo model, summarizing key operational insights and strategic 
                recommendations for decision-making."""),
            callback=self.append_event_callback,
            context=tasks,
            output_json=AccountInfo,
        )
    
    # @traceable(name="review research", run_type="prompt", process_inputs=debug_process_inputs)    
    def manage_research(self, agent: Agent, target_account: str, topic: str, tasks: list[Task]):
        return Task(            
            description=dedent(f"""
                For the {target_account}, establish research objectives for each {topic}, and oversee the integration of account and strategy 
                research, ensuring operational data and strategic insights are seamlessly combined. Monitor all subtopic data collection to align 
                with your objectives, providing specific guidance and feedback to direct research outcomes effectively.                
                
                Action Items:
                1. Define Topic Research Objectives:
                - Establish clear and strategic objectives for each {topic} related to the {target_account}.
                - Communicate these objectives to the Account and Strategic Researchers to guide their data gathering process.
                2. Develop Subtopics to Support Topics:
                - Evaluate the initial data collected to ensure it aligns with the set topic objectives.
                - Provide feedback that directs further data gathering and refines subtopics for alignment and depth.
                3. Provide Oversight:
                - Continuously guide the Account Researcher with strategic insights and feedback.
                - Ensure the alignment of the research with the strategic goals of the report.

                Guidelines:
                - Ensure research findings are derived from the most current and credible sources.
                - Use focused keywords and strategic queries to guide detailed research efforts.
                - Maintain a critical evaluation of all research outputs to ensure alignment with the set objectives.
                """),            
            agent=agent,
            expected_output=dedent(f"""
                A well-defined TopicInfo model that encapsulates coherent subtopics, aligning operational data with strategic 
                opportunities for comprehensive reporting."""),
            callback=self.append_event_callback,
            context=tasks,
            output_json=TopicInfo,
        )

    # @traceable(name="research strategy", run_type="retriever", process_inputs=debug_process_inputs)    
    def research_strategy(self, agent: Agent, target_account: str, topic: str, tasks: list[Task]):
        return Task(
            description=dedent(f"""
                Research and compile strategic initiatives relevant to {target_account}'s using authoritative sources.
        
                Action Items:
                - Gather insights from McKinsey Quantum Black, Deloitte, KPMG, PwC, BCG, and Accenture focused on industry analysis.
                - Align your research with the objectives for each {topic} as communicated by the Research Manager.
                - Prioritize recent studies, white papers, and reports discussing relevant solutions.
                - Submit initial findings for review and refine based on feedback from the Research Manager.
        
                Guidelines:
                - Ensure all sources are recent and reputable, providing detailed insights into real world applications.
                - Use targeted searches and keywords to explore specific solutions for identified operational challenges.
                """),
            agent=agent,
            expected_output=dedent("""
                A detailed compilation of `SubTopic` models summarizing detailing AI/ML strategies within the {target_account}'s industry, each enriched 
                with strategically gathered information from primary sources."""),
            callback=self.append_event_callback,
            context=tasks,
            output_json=SubTopic,
            async_execution=True
        )

    # @traceable(name="research account", run_type="retriever", process_inputs=debug_process_inputs)    
    def research_account(self, agent: Agent, target_account: str, topic: str):
        return Task(
            description=dedent(f"""
                Conduct thorough research to gather detailed operational information for {target_account} for each {topic} following 
                direction from the research manager. Ensure the process focuses on the most authoritative sources to support insightful analysis.
                                
                Action Items:
                - Prioritize information from the company's official website, latest annual report, recent press releases, and other 
                official publications.
                - Ensure that all sources are recent (within the last 4 years) and highly credible.
                - Submit initial findings for preliminary review and refine based on feedback.
                - Dynamically craft new queries using relevant keywords when initial searches do not yield necessary information, 
                this ensures comprehensive coverage of each topic.
                """),
            agent=agent,
            expected_output=dedent("""
                A detailed compilation of `SubTopic` models summarizing key operational data about {target_account}, each enriched 
                with strategically gathered information from primary sources. ."""),
            callback=self.append_event_callback,
            output_json=SubTopic,
            async_execution=True
        )



    # @traceable(name="review research", run_type="prompt", process_inputs=debug_process_inputs)    
    # def write_report(self, agent: Agent, target_account: str, topics: list[str], tasks: list[Task]):
    #     return Task(            
    #         agent=agent,
    #         description=dedent(f"""
    #             Assemble a comprehensive document detailing the research findings, strategic insights, and analysis related to 
    #             the {target_account}. This document should integrate all the collected information, analysis, and insights from 
    #             the research team, providing a complete picture of the account in an easily digestible format.

    #             Action Items:
    #             - Synthesize information from the 'TopicInfo' and 'Finding' JSON objects developed by the research team.
    #             - Ensure the report includes essential details like key challenges, strategic opportunities, the source of all information used.
    #             - Each of the {topics} needs a minimum of 3-5 findings.
    #             - Review and incorporate feedback from the initial research and refined research stages to ensure completeness and accuracy.
                
    #             Guidelines:
    #             - Every finding must include a source title, URL, and year published.
    #             - Use clear, concise language to ensure readability and ease of understanding.
    #             - Include summaries of the most relevant findings and strategic points.
    #             - Provide context and implications of the research to guide decision-making in the report.
    #             """),
    #         expected_output=dedent(
    #             """A 'AccountInfo' JSON object compiled as a list of 'TopicInfo' JSON objects, each written in clear, concise language"""),
    #         callback=self.append_event_callback,
    #         context=tasks,
    #         output_json=AccountInfo,
    #     )
    
    # @traceable(name="review research", run_type="prompt", process_inputs=debug_process_inputs)    
    # def manage_research(self, agent: Agent, target_account: str, topics: list[str], tasks: list[Task]):
    #     return Task(            
    #         description=dedent(f"""
    #             Review and refine a comprehensive 'TopicInfo' JSON object for the {target_account} for each specified of the {topics}. 
    #             Develop strategic research points, questions, and discussion angles for the report to guide what research is conducted.
    #             Evaluate sourceinfo and highlights collected by the Account Researcher to ensure alignment with strategic research objectives.
                
    #             Action Items:
    #             - Prioritize recent and credible sources such as official company websites, annual reports, and relevant press releases.
    #             - Suggest secondary sources like industry analyses and business news for broader context.
    #             - Rank all sources based on their relevance to the research objectives.
    #             - If the Account Researcher has not included key content, advise on what to extract or analyze further.
    #             - Provide clear, actionable feedback to refine the researcher's approach.
    #             """),            
    #         agent=agent,
    #         expected_output=dedent(
    #             """A 'TopicInfo' JSON object compiled as a list of 'Finding' JSON objects, each meticulously evaluated for relevance 
    #             and accuracy."""),
    #         callback=self.append_event_callback,
    #         context=tasks,
    #         output_json=TopicInfo,
    #     )

    # @traceable(name="research account", run_type="retriever", process_inputs=debug_process_inputs)    
    # def research_account(self, agent: Agent, target_account: str, topics: list[str]):
    #     return Task(
    #         description=dedent(f"""
    #             Conduct in-depth research and create detailed 'finding' JSON objects for the {target_account} and each of the 
    #             specified research {topics}. The task is segmented into three phases: Initial Research, Follow-up Based on Feedback, 
    #             and Compilation of 'Finding' JSON Objects.
                
    #             Action Items:
    #             1. Initial Research:
    #             - Identify and gather 'sourceinfo' with relevant information to the research topics.
    #             - Submit for preliminary review.
    #             2. Follow-up Based on Feedback:
    #             - Enhance data depth based on feedback adjusting your research approach 
    #             - Collect more targeted data with enriched data details and submit for review.
    #             3. Compilation of 'Finding' JSON Objects:
    #             - Compile the final findings into comprehensive JSON objects.
    #             - 'Finding' JSON object includes essential elements such as title, URL, publication year, and 3-5 snippets.

    #             Important Guidelines:
    #             - Do not fabricate information; only include data found in the URLs.
    #             - Prioritize recent information by limiting sources to those from the last 4 years.
    #             """),
    #         agent=agent,
    #         expected_output="A 'Finding' JSON object",
    #         callback=self.append_event_callback,
    #         output_json=FindingInfo,
    #         async_execution=True
    #     )
