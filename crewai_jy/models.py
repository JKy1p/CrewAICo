from typing import List, Union
from pydantic.v1 import BaseModel, HttpUrl


# Model for Referencing Information 
class Source(BaseModel):
    source_title: str = "Default Title"
    url: Union[str, HttpUrl] = "http://example.com"
    year_published: int = 2022

# Next level up, incorporates Source with snippets
class SourceInfo(BaseModel):
    source_from: Source = Source()
    snippets: List[str] = ["snippet1", "snippet2"]

# More complex model, built from SourceInfo
class FindingInfo(BaseModel):
    finding_title: str = "Default Finding"
    finding_insight: str = "Default insight"
    finding_info: List[SourceInfo] = [SourceInfo()]

# Top level model, built from FindingInfo
class TopicInfo(BaseModel):
    topic_title: str = "Topic"
    topic_insights: List[str] = ["Insight1", "Insight2"]
    topic_info: List[FindingInfo] = [FindingInfo()]


    
    
    

