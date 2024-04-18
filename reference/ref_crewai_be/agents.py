from typing import List
from textwrap import dedent
from crewai import Agent
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool
from tools.youtube_search_tools import YoutubeVideoSearchTool


class CompanyResearchAgents():

    def __init__(self):
        self.searchInternetTool = SerperDevTool()
        self.youtubeSearchTool = YoutubeVideoSearchTool()
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def research_reviewer(self, target_account: str, topics: List[str]) -> Agent:
        return Agent(
            role="Account Research Reviewer",
            goal=f"""Generate a list of JSON objects containing the urls for 3 recent blog articles and 
                the url and title for 3 recent YouTube interview, for each position in each company.
             
                Companies: {target_account}
                Positions: {topics}

                Important:
                - The final list of JSON objects must include all companies and positions. Do not leave any out.
                - If you can't find information for a specific position, fill in the information with the word "MISSING".
                - Do not generate fake information. Only return the information you find. Nothing else!
                - Do not stop researching until you find the requested information for each position in each company.
                - All the companies and positions exist so keep researching until you find the information for each one.
                - Make sure you each researched position for each company contains 3 blog articles and 3 YouTube interviews.
                """,
            backstory="""As a Company Research Manager, you are responsible for aggregating all the researched information
                into a list.""",
            llm=self.llm,
            tools=[self.searchInternetTool, self.youtubeSearchTool], # TODO Add tools
            verbose=True,
            allow_delegation=True
        )

    def account_researcher(self) -> Agent:
        return Agent(
            role="Company Research Agent",
            goal="""Look up the specific positions for a given company and find urls for 3 recent blog articles and 
                the url and title for 3 recent YouTube interview for each person in the specified positions. It is your job to return this collected 
                information in a JSON object""",
            backstory="""As a Company Research Agent, you are responsible for looking up specific positions 
                within a company and gathering relevant information.
                
                Important:
                - Once you've found the information, immediately stop searching for additional information.
                - Only return the requested information. NOTHING ELSE!
                - Make sure you find the persons name who holds the position.
                - Do not generate fake information. Only return the information you find. Nothing else!
                """,
            tools=[self.searchInternetTool, self.youtubeSearchTool], # TODO Add tools
            llm=self.llm,
            verbose=True
        )
