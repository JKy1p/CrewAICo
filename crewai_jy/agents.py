from typing import List
from textwrap import dedent 
from crewai import Agent
from langchain_openai import ChatOpenAI
from tools.exa_search_tool import ExaSearchToolset
from langsmith import traceable
from langchain_community.llms import Ollama
from utils.logging import logger

@traceable
class AccountResearchAgents():

    def __init__(self, **data):
        tools = ExaSearchToolset.tools()
        self.search = tools[0]
        self.find_similar = tools[1]
        self.get_contents = tools[2]
        self.ollama_llm = Ollama(model="mistral:7b-instruct")
        # self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    @traceable(name="agent.research_reviewer")    
    def research_reviewer(self, target_account: str, topics: List[str], **data) -> Agent:
        return Agent(
            role="Research Reviewer",
            goal=dedent(f"""\
                Your goal is to create a list of JSON objects with precise and pertinent findings for {target_account} related to the {topics}. 
                You'll validate the research quality, identifying gaps for the account_researcher to explore further. Through iterative feedback 
                focused on operations and strategy, refine the JSON objects with strategic precision.

                Target Account: {target_account}
                Research Topics: {topics}

                Important:
                - The final list of JSON objects must include all 'findings' topic, ensure they are collected
                - Ensure all findings within a topic are supported by credible sources and provided.
                - Exclude unverified info for accuracy, and mark unavailable data as "MISSING" to maintain integrity.
                - Directing the research_agent to refine their search and analysis by giving clear, actionable feedback
                - Do not stop iterating until findings are high-quality, comprehensive for each research topic.
                """),
            backstory=dedent("""\
                As the Account Research Reviewer, your mission  is to pinpoint crucial  information for a thorough understanding of the target account. 
                This entails analyzing  research findings, and addressing the  gaps by providing the researchers new search strategies and the context. 
                Your  executive experience in business operations and strategy is vital in formulating specific queries for the researchers and judging 
                sources to discard irrelevant information.
                """),
            llm=self.ollama_llm,
            verbose=True,
            allow_delegation=True
        )
    
    @traceable(name="agent.account_researcher")    
    def account_researcher(self, **data) -> Agent:   
        return Agent(
            role="Account Researcher",
            goal=dedent("""\
            As the Account Researcher, your task is to conduct thorough searches on designated topics for a target_account, identifying relevant URLs 
            and extracting detailed information. Your expertise lies in managing complex queries, interpreting context, and sourcing from a wide array 
            of formats, including web pages and web accessible PDFs. You are responsible for compiling this information into a concise, structured JSON object.
            """),
            backstory="""As the Account Researcher, your mission is to gather comprehensive information on the target_account's current operations. You
            retrieve pertinent details about the target_account's business model, products and services, market strategy, and operational challenges. 
            """,
            tools= [self.search, self.find_similar, self.get_contents],
            llm=self.ollama_llm,
            verbose=True
        )



