from functools import partial
import ast
from typing import Type, List, Dict, Callable, Any, Optional, Union
from datetime import datetime
import os
from exa_py.api import Exa 
from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field
from crewai_tools import BaseTool
from langsmith import traceable
import traceback
from typing import List
from exa_py.api import ResultWithHighlights

# Define the SearchResult model
class SearchResult(BaseModel):  
    id: str
    title: str
    year:int
    url: str
    snippet: str
    highlights: List[str]
    finding: str
    topic: str
    
@traceable
class ExaSearchInput(BaseModel):
    target_account: str = Field(..., description="The target account name for the search.")
    topic: str = Field(..., description="The topics of interest for the search.")
    limit: Optional[int] = 3

    @property
    def query(self) -> str:
        # Form the query from target_account and topic
        return f"{self.target_account} {self.topic}"

class ExaSearchToolset:
    
    @tool
    @traceable(name="tool.search")
    def search(query: str):  # type: ignore
        """Search for a webpage based on the query and retrieve titles, URLs, and snippets."""
        return ExaSearchToolset._exa().search_and_contents(
            query=query,
            highlights=True,  
            use_autoprompt=True,
            num_results=3  # Adjust the number of results as needed
        )    
    @tool
    @traceable(name="tool.find_similar")
    def find_similar(url: str): # type: ignore
        """
        Search for webpages similar to a given URL and retrieve titles, URLs, and snippets.
        The URL passed in should be a URL returned from `search`.
        """
        return ExaSearchToolset._exa().find_similar_and_contents(
            url=url,
            highlights=True,  
            num_results=3  
        )
    @tool
    @traceable(name="tool.get_contents")
    def get_contents(ids: Union[str, List[str]]): # type: ignore
        """
        Get the highlights of a webpage based on the provided IDs.
        The ids must be passed in as a list, a list of ids returned from `search`.
        """
        # Ensure ids are in the correct format (a list of strings)
        if isinstance(ids, str):
            ids = [ids]  # Convert a single string to a list for consistency

        response = ExaSearchToolset._exa().get_contents(ids, highlights=True)

        # Process and format the highlights for display or further processing
        formatted_contents = []
        for result in response.results:
            if isinstance(result, ResultWithHighlights):
                # Format each result with its URL, title, highlights, and their scores
                entry = f"URL: {result.url}\nTitle: {result.title}\nHighlights and Scores:\n"
                entry += "\n".join(f"- {highlight} (Score: {score:.2f})"
                    for highlight, score in zip(result.highlights, result.highlight_scores))
                formatted_contents.append(entry)
            else:
                # Fallback entry if no highlights are available
                formatted_contents.append(f"URL: {result.url}\nTitle: {result.title}\nNo highlights available.")

        return "\n\n".join(formatted_contents)
        

    @staticmethod
    def tools():
        return [
            ExaSearchToolset.search,
            ExaSearchToolset.find_similar,
            ExaSearchToolset.get_contents
        ]

    @staticmethod
    def _exa():
        return Exa(api_key=os.environ.get('EXA_API_KEY'))
# Example of using the class
    


















        
    
    


