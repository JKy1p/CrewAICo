from typing import List, TypeVar, Generic, Optional 
import os, json
from exa_py.api import Exa, SearchResponse
from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field, HttpUrl
from crewai_tools import BaseTool
from langsmith import traceable
from utils.logging import debug_process_inputs
from exa_py.api import Exa

# Define the SearchResult model
class SearchResult(BaseModel):
    id: str
    url: HttpUrl
    title: str
    text: Optional[str] = None
    highlights: Optional[List[str]] = None
    highlight_scores: Optional[List[float]] = None     
    
                
class ExaSearchInput(BaseModel):
    target_account: str = Field(..., description="The target account for the search.")
    topic: str = Field(..., description="The topics of interest for the search.")
    limit: Optional[int] = 3

    @property
    def query(self) -> str:
        return f"{self.target_account} {self.topic}"

class ExaSearchToolset(BaseTool):
    @tool
    def search(search_input: ExaSearchInput) -> SearchResponse[SearchResult]: # type: ignore
        """Search for a webpage based on the query constructed from search input."""
        query = search_input.query        
        return ExaSearchToolset._exa().search(query, use_autoprompt=True, num_results=3)


    @tool
    def find_similar(url: str) -> SearchResponse[SearchResult]: # type: ignore
        """Search for webpages similar to a given URL."""

        return ExaSearchToolset._exa().find_similar(url, num_results=3)

    @tool
    def get_contents(ids_str: str) -> str: # type: ignore
        """
        Get the contents of a webpage.
        The ids must be passed in as a JSON string representing a list of ids.
        """
        try:
            ids = json.loads(ids_str)  # Safely convert string to list
        except json.JSONDecodeError:
            return "Invalid input format."

        contents = str(ExaSearchToolset._exa().get_contents(ids))
        contents = contents.split("URL:")
        contents = [content[:1000] for content in contents]
        return "\n\n".join(contents)

    @staticmethod
    def _exa():
        return Exa(api_key=os.environ.get('EXA_API_KEY'))

    @staticmethod
    def tools():
        return [
            ExaSearchToolset.search,
            ExaSearchToolset.find_similar,
            ExaSearchToolset.get_contents
        ]
# Example of using the class
    

    
    # @tool
    # @traceable(name="find similar", run_type="tool", process_inputs=debug_process_inputs)    
    # def find_similar(url: str): # type: ignore
    #     """
    #     Search for webpages similar to a given URL and retrieve titles, URLs, and snippets.
    #     The URL passed in should be a URL returned from `search`.
    #     """
    #     return ExaSearchToolset._exa().find_similar_and_contents(
    #         url=url,
    #         highlights=True,  
    #         num_results=3  
    #     )
    # @tool
    # @traceable(name="get contents", run_type="tool", process_inputs=debug_process_inputs)    
    # def get_contents(ids: Union[str, List[str]]): # type: ignore
    #     """
    #     Get the highlights of a webpage based on the provided IDs.
    #     The ids must be passed in as a list, a list of ids returned from `search`.
    #     """
    #     # Ensure ids are in the correct format (a list of strings)
    #     if isinstance(ids, str):
    #         ids = [ids]  # Convert a single string to a list for consistency

    #     response = ExaSearchToolset._exa().get_contents(ids, highlights=True)

    #     # Process and format the highlights for display or further processing
    #     formatted_contents = []
    #     for result in response.results:
    #         if isinstance(result, ResultWithHighlights):
    #             # Format each result with its URL, title, highlights, and their scores
    #             entry = f"URL: {result.url}\nTitle: {result.title}\nHighlights and Scores:\n"
    #             entry += "\n".join(f"- {highlight} (Score: {score:.2f})"
    #                 for highlight, score in zip(result.highlights, result.highlight_scores))
    #             formatted_contents.append(entry)
    #         else:
    #             # Fallback entry if no highlights are available
    #             formatted_contents.append(f"URL: {result.url}\nTitle: {result.title}\nNo highlights available.")

    #     return "\n\n".join(formatted_contents)
        

    # @staticmethod
    # def tools():
    #     return [
    #         ExaSearchToolset.search,
    #         ExaSearchToolset.find_similar,
    #         ExaSearchToolset.get_contents
    #     ]

    # @staticmethod
    # def _exa():
    #     return Exa(api_key=os.environ.get('EXA_API_KEY'))

















        
    
    


