import os
from abc import abstractmethod, ABC
from typing import Any, Callable, Dict, Type 
from pydantic.v1 import BaseModel, Field 
from exa_py.api import Exa
from crewai_tools import BaseTool
from langsmith import traceable


# Define the SearchResult model
class SearchResult(BaseModel):
    id: str
    title: str
    url: str
    date_published: str
    snippet: str

# Define the input model for Exa search
class ExaSearchInput(BaseModel):
    target_account: str = Field(..., description="The target account for the search.")
    topic: str = Field(..., description="The topics of interest for the search.")

# Define the abstract BaseTool class
class BaseTool(ABC):
    @abstractmethod
    def _run(self, *args: Any, **kwargs: Any) -> Any:

# Define the ExaSearchToolset class
class ExaSearchToolset(BaseTool):
    def __init__(self, name: str, description: str, args_schema: Type[BaseModel] = ExaSearchInput, description_updated: bool = False):
        self.name = name
        self.description = description
        self.args_schema = args_schema
        self.description_updated = description_updated
        # Mapping tool names to their corresponding methods
        self.tool_dispatch: Dict[str, Callable] = {
            "search": self.search,
            "find_similar": self.find_similar,
            "get_contents": self.get_contents
        }

    def _run(self, tool_name: str, *args: Any, **kwargs: Any) -> Any:
        tool_method = self.tool_dispatch.get(tool_name)
        if tool_method:
            return tool_method(*args, **kwargs)
        else:
            raise ValueError(f"Tool {tool_name} is not a valid method name.")

    def search(self, target_account: str, topic: str):
        """Search for a webpage based on the target account and topic."""
        query = f"Find information on {topic} related to {target_account}"
        # This is a placeholder for the actual search logic
        return f"Searching for {query}"

    def find_similar(self, url: str):
        """Search for webpages similar to a given URL."""
        # This is a placeholder for the actual find_similar logic
        return f"Finding pages similar to {url}"

    def get_contents(self, ids: str):
        """Get the contents of a webpage."""
        # This is a placeholder for the actual get_contents logic
        ids_list = ids.strip("[]").split(",")
        ids_list = [id.strip().strip("'\"") for id in ids_list]
        # Simulate fetching content for each ID
        contents = [f"Content for {id}" for id in ids_list]
        return "\n\n".join(contents)

    def _exa(self):
        """Initializes and returns an Exa client instance."""
        # This is a placeholder for the actual Exa client initialization
        return "Exa client instance"

# Note: The actual Exa client initialization and search/find_similar/get_contents logic would need to interact with the Exa API, 
# which requires network calls not shown here. This code provides a structure and mock implementations for illustration.









































# class SearchResult(BaseModel):
#     id: str
#     title: str
#     url: str
#     date_published: str
#     snippet: str

# class ExaSearchInput(BaseModel):
#     target_account: str = Field(..., description="The target account for the search.")
#     topic: str = Field(..., description="The topics of interest for the search.")


# class ExaSearchToolset(BaseTool):
#     name: str
#     description: str
#     args_schema: Type[BaseModel] = ExaSearchInput
        
#     def search(self, target_account: str, topic: str):
#         """Search for a webpage based on the target account and topic."""
#         query = f"Find information on {topic} related to {target_account}"
#         return self._exa().search(query, use_autoprompt=True, num_results=3)
    
#     def find_similar(self, url: str):
#         """Search for webpages similar to a given URL."""
#         return self._exa().find_similar(url, num_results=3)

#     def get_contents(self, ids: str):
#         """Get the contents of a webpage."""
        
#         ids_list = ids.strip("[]").split(",")
#         ids_list = [id.strip().strip("'\"") for id in ids_list]  
#         contents = str(self._exa().get_contents(ids_list))
#         contents = contents.split("URL:")
#         contents = [content[:1000] for content in contents]
#         return "\n\n".join(contents)            
    
#     def _exa(self):
#         """Initializes and returns an Exa client instance."""
#         return Exa(api_key=os.environ.get('EXA_API_KEY'))

    
#     def tools(self) -> List[Callable]:
#         return [
#             self.search,
#             self.find_similar,
#             self.get_contents
#         ]
    




