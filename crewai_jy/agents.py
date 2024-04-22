from typing import List
from textwrap import dedent 
from crewai import Agent
from tools.exa_search_tool import ExaSearchToolset
from langchain_openai import ChatOpenAI
from langsmith import traceable
from langchain_community.llms import Ollama
from utils.logging import logger, debug_process_inputs

@traceable
class AccountResearchAgents():

    def __init__(self):
        self.searchExaTool = ExaSearchToolset()
        # self.ollama_llm = Ollama(model="llama3:instruct")
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
        # self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def report_writer(self, target_account: str, topics: List[str]) -> Agent:
        return Agent(
            role="Research Writer",
            goal=dedent(f"""\
                Compile and synthesize the collected operational data into a detailed report that highlights key findings, insights, and strategic recommendations 
                for the {target_account}. Set clear objectives for the report's structure and content at the AccountInfo level, ensuring all necessary information 
                is included for strategic decision-making.
                """),
            backstory=dedent("""\
                As a skilled Writer with a background in technical writing and journalism, you excel at distilling complex operational data into clear, compelling 
                narratives. Your role is crucial in bridging intricate research findings with strategic business applications, ensuring the report not only summarizes 
                the research but also provides actionable insights and recommendations.
                """),
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )
    
    @traceable(name="research_reviewer", run_type="llm", process_inputs=debug_process_inputs)    
    def research_manager (self, target_account: str, topics: List[str]) -> Agent:
        return Agent(
            role="Research Manager",
            goal=dedent(f"""
                Direct and enhance the research process for the {target_account}, refining the collected data and guiding the development of comprehensive topics. 
                It is your responsibility to set the topic objectives, review researcher outputs, and identify strategic keywords for further research queries. This 
                ensure that all subtopics align with your overarching topic goals.
                """),
            backstory=dedent("""\
                As a Research Manager, your role combines oversight of research outcome with expert knowledge in operations and strategy analysis. You guide the development 
                of the report structure and content, ensuring that all research supports topic objects. Your critical evaluations of initial research outputs bridge 
                the gap between raw data and actionable insights, directing the research focus to meet the objectives you have established for each topic.
                """),
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )
    
    @traceable(name="strategy researcher", run_type="llm", process_inputs=debug_process_inputs)    
    def strategy_researcher(self) -> Agent:   
        return Agent(
            role="AI/ML Strategy Researcher",
            goal=dedent("""
                Investigate and gather strategic insights specifically tailored to address actionable opportunities within {target_account}'s 
                operations. Specific sites for source information include McKinsey Quantum Black, Deloitte, KPMG, PwC, BCG, and Accenture.
                """),
            backstory=dedent("""
                As a Strategy Researcher, you transform operational insights into strategic initiatives using your deep understanding of industry trends and 
                data-driven analysis. This vital role develops forward-looking strategies that are effective and actionable, relying on the most relevant and 
                reliable data.
                """),
            tools=[self.searchExaTool],  
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )

    
    @traceable(name="account researcher", run_type="llm", process_inputs=debug_process_inputs)    
    def account_researcher(self) -> Agent:   
        return Agent(
            role="Account Researcher",
            goal=dedent("""Gather comprehensive operational data on {target_account} on specified research {topics}, focusing on the most credible and current 
                sources such as the company's website, latest annual reports, press releases and official publications.
                """),
            backstory=dedent("""
                As an Account Researcher, you are armed with strong analytical skills and a strategic approach to data gathering, the Account Researcher specializes 
                in uncovering and structuring key operational information. This foundational stage sets the groundwork for in-depth analysis and strategic decisions, 
                leveraging only the most official and relevant data sources.
                """),
            tools=[self.searchExaTool],  
            llm=self.llm,
            verbose=True,
        )



    # @traceable(name="research_reviewer", run_type="llm", process_inputs=debug_process_inputs)    
    # def research_reviewer(self, target_account: str, topics: List[str], **data) -> Agent:
    #     return Agent(
    #         role="Research Reviewer",
    #         goal=dedent(f"""\
    #             Your goal is to create a list of JSON objects with precise and pertinent findings for {target_account} related to the {topics}. 
    #             You'll validate the research quality, identifying gaps for the account_researcher to explore further. Through iterative feedback 
    #             focused on operations and strategy, refine the JSON objects with strategic precision.

    #             Target Account: {target_account}
    #             Research Topics: {topics}

    #             Important:
    #             - The final list of JSON objects must include all 'findings' topic, ensure they are collected
    #             - Ensure all findings within a topic are supported by credible sources and provided.
    #             - Exclude unverified info for accuracy, and mark unavailable data as "MISSING" to maintain integrity.
    #             - Directing the research_agent to refine their search and analysis by giving clear, actionable feedback
    #             - Do not stop iterating until findings are high-quality, comprehensive for each research topic.
    #             """),
    #         backstory=dedent("""\
    #             As the Account Research Reviewer, your mission  is to pinpoint crucial  information for a thorough understanding of the target account. 
    #             This entails analyzing  research findings, and addressing the  gaps by providing the researchers new search strategies and the context. 
    #             Your  executive experience in business operations and strategy is vital in formulating specific queries for the researchers and judging 
    #             sources to discard irrelevant information.
    #             """),
    #         llm=self.ollama_llm,
    #         verbose=True,
    #         allow_delegation=True
    #     )
    
    # @traceable(name="account researcher", run_type="llm", process_inputs=debug_process_inputs)    
    # def account_researcher(self, **data) -> Agent:   
    #     return Agent(
    #         role="Account Researcher",
    #         goal=dedent("""\
    #         As the Account Researcher, your task is to conduct thorough searches on designated topics for a target_account, identifying relevant URLs 
    #         and extracting detailed information. Your expertise lies in managing complex queries, interpreting context, and sourcing from a wide array 
    #         of formats, including web pages and web accessible PDFs. You are responsible for compiling this information into a concise, structured JSON object.
    #         """),
    #         backstory="""As the Account Researcher, your mission is to gather comprehensive information on the target_account's current operations. You
    #         retrieve pertinent details about the target_account's business model, products and services, market strategy, and operational challenges. 
    #         """,
    #         tools= [self.search, self.find_similar, self.get_contents],
    #         llm=self.ollama_llm,
    #         verbose=True,
    #     )
