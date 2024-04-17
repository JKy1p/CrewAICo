from functools import partial
import ast
from typing import Type, List, Dict, Callable, Any, Optional
from pydantic.v1 import BaseModel, Field
from datetime import datetime
import os
from exa_py.api import Exa
from langchain_core.tools import tool
from crewai_tools import BaseTool
from langsmith import traceable
import traceback

# Define the SearchResult model
class SearchResult(BaseModel):
    
    id: str
    title: str
    url: str
    date_published: datetime
    finding: str
    description: str

class ExaSearchInput(BaseModel):
    target_account: str = Field(..., description="The target account for the search.")
    topic: str = Field(..., description="The topics of interest for the search.")
    limit: Optional[int] = 10

    @property
    def query(self) -> str:
        # Form the query from target_account and topic
        return f"{self.target_account} {self.topic}"
    
class ExaSearchToolset(BaseTool):
    name: str = "exa_search_toolset"
    description: str = "A toolset for searching Exa."
    args_schema: Type[BaseModel] = ExaSearchInput
    tool_dispatch: Any = None
    
    def __init__(self) -> None:
        super().__init__(name="exa_search_toolset", description="A toolset for searching Exa.")
        self._exa_instance = Exa(api_key=os.environ.get('EXA_API_KEY'))  
        self.tool_dispatch = {}
        for name, method in type(self).__dict__.items():
            if callable(method) and hasattr(method, "_tool"):
                self.tool_dispatch[name] = partial(method, self)
                
    def _exa(self):
        """
        Returns an instance of the Exa class for interacting with the Exa API.
        """
        if not hasattr(self, '_exa_instance') or self._exa_instance is None:
            self._exa_instance = Exa(api_key=os.environ.get('EXA_API_KEY'))
        return self._exa_instance
    
    def _run(self, tool_name: str, **kwargs: Any) -> Any:
        try:
            # Get the tool method
            tool_method = self.tool_dispatch.get(tool_name)
            if not tool_method:
                raise ValueError(f"Tool {tool_name} is not a valid method name.")

            # Call the tool method with the provided arguments
            return tool_method(**kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            
    @tool
    def _run_search(self, query: str, target_account: str, topic: str) -> Tool:
        """Search for a webpage based on the target account and topic."""
        query = f"Find information on {topic} related to {target_account}"
        # This is a placeholder for the actual search logic
        return self._exa().search(query, use_autoprompt=True, num_results=3)        
    @tool
    def _run_find_similar(self, url: str):
        """
        Finds content similar to the given URL, with customizable filtering and result options.

        This function performs a search to find content similar to that of the specified URL, allowing for detailed control over the search through various parameters. 
        
        Args:
            url (str): The URL of the content to find similar results for.
            num_results (Optional[int], optional): The maximum number of results to return.

        Returns:
            SearchResponse[_Result]: A response object containing the similar search results, which may include an autoprompt string if applicable.
        """
        return self._exa().find_similar(url, num_results=3)
    
    @tool
    def _run_get_contents(self, ids: str):
        """
        Retrieves the content for a given set of identifiers, with options for including text contents.

        This method supports multiple types of identifiers (single ID, list of IDs, or list of result objects) and allows for detailed control over the inclusion of text contents through the 'text' parameter. The text contents can either be included as is or customized according to the provided TextContentsOptions.

        Args:
        ids (Union[str, List[str], List[_Result]]): The identifier(s) for the content(s) to retrieve. This can be a single ID, a list of IDs, or a list of result objects.
        text (Union[TextContentsOptions, Literal[True]]): Specifies how text content should be included in the response. This can be a boolean value (True to include text contents as is) or an instance of TextContentsOptions to specify more detailed text content inclusion criteria.

        Returns:
        SearchResponse[ResultWithText]: A response object containing the results with their associated text contents, if requested.

        Note:
        This is an overloaded function definition intended for type hinting and documentation purposes. It describes one possible way to call the 'get_contents' method, focusing on scenarios where text content inclusion is specified.
        """
        ids = ast.literal_eval(ids)

        contents = str(self._exa().get_contents(ids))
        contents = contents.split("URL:")
        contents = [content[:1000] for content in contents]
        return "\n\n".join(contents)
    
    def run_tool(self, tool_name: str, **kwargs):
        tool_method = getattr(self, tool_name, None)
        if tool_method is None:
            raise ValueError(f"No tool named '{tool_name}' found.")
        return tool_method(**kwargs)    
    
    def tools(self):
        return [
            self._run_search,
            self._run_find_similar,
            self._run_get_contents
        ]
    


















        
    
    


