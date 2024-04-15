from typing import List
from pydantic import BaseModel


class NamedUrl(BaseModel):
    title: str 
    url: str 
    year: int
    snippet: str
    
class NamedUrlList(BaseModel):
    id: str
    urls: List[NamedUrl]
    
class Finding(BaseModel):
    title: str
    source: NamedUrl
    highlights: List[str]

class TopicInfo(BaseModel):
    title: str
    topic: List[Finding]
    additional_sources: List[NamedUrl]
    
class TopicInfoList(BaseModel):
    topics: List[TopicInfo]
