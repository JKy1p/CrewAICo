from functools import partial
import ast
from typing import Type, List, Dict, Callable, Any, Optional, Union, ClassVar
from datetime import datetime
import os
from exa_py.api import Exa 
from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field
from crewai_tools import BaseTool
from langsmith import traceable
from utils.logging import debug_process_inputs
from exa_py.api import Exa
from models import Source
from crewai_tools import BaseTool
from models import Source
import json

# Define the SearchResult model
class SearchResult(BaseModel):  
    number: int
    source: str
    text: str
    highlights: List[str]
    
    def __iter__(self):
        """
        Allow iteration over the model's fields, yielding key-value pairs
        of field names and their values.
        """
        for field, value in self.dict().items():
            yield (field, value)
    
    
class ExaSearchInput(BaseModel):
    target_account: str = Field(..., description="The target account for the search.")
    topic: str = Field(..., description="The topics of interest for the search.")
    limit: Optional[int] = Field(default=10, description="Maximum number of results to return")

    @property
    def query(self) -> str:
        return f"{self.target_account} {self.topic}"

class ExaSearchToolset(BaseTool):

    @staticmethod
    @tool
    def search(search_input: ExaSearchInput) -> List[SearchResult]:
        """Search for a webpage based on the query constructed from search input."""
        query = search_input.query
        raw_results = ExaSearchToolset._exa().search(query, use_autoprompt=True, num_results=search_input.limit)
        return [SearchResult(**result) for result in raw_results]

    @staticmethod
    @tool
    def find_similar(url: str) -> List[SearchResult]:
        """
        Search for webpages similar to a given URL.
        The URL passed in should be a URL returned from `search`.
        """
        raw_results = ExaSearchToolset._exa().find_similar(url, num_results=3)
        return [SearchResult(**result) for result in raw_results]

    @staticmethod
    @tool
    def get_contents(ids: List[str]) -> str:
        """
        Get the contents of a webpage.
        The ids must be passed in as a list, a list of ids returned from `search`.
        """
        try:
            ids = json.loads(ids_str)  # Safely convert string to list
        except json.JSONDecodeError:
            return "Invalid input format."

        contents = ExaSearchToolset._exa().get_contents(ids)
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

















        
    
    


