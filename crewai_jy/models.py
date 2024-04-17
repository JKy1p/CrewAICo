from typing import List
from pydantic import BaseModel, HttpUrl 


class Source(BaseModel):
    number: int
    source_title: str 
    url: HttpUrl 
    date_published: int
    
class SourceInfo(BaseModel):
    source_info_title: Source
    highlights: List[str]
    
class Finding(BaseModel):
    finding_title: str
    text: str
    highlights: List[str]
    finding_info: List[SourceInfo]

class TopicInfo(BaseModel):
    topic_title: str
    text: str
    highlights: List[str]
    topic_info: List[Finding]
    
# class TopicInfoList(BaseModel):
#     topics: List[TopicInfo]
