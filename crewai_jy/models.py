from typing import List, Union
from pydantic import BaseModel, HttpUrl


# Model for Referencing Information 
class Source(BaseModel):
    source_title: str = "Default Title"
    url: Union[str, HttpUrl] = "http://example.com"
    year_published: int = 2022

# Next level up, incorporates Source with snippets
class SourceInfo(BaseModel):
    source_from: List[Source] 
    highlights: List[str] = ["highlight1", "highlight2"]

# More complex model, built from SourceInfo
class FindingInfo(BaseModel):
    finding_title: str = "Default Finding"
    finding_insight: str = "Default insight"
    finding_info: List[SourceInfo]

# Top level model, built from FindingInfo
class TopicInfo(BaseModel):
    topic_title: str = "Topic"
    topic_insights: List[str] = ["Insight1", "Insight2"]
    topic_info: List[FindingInfo] 

# class ResearchOutput(BaseModel):
#     source: Source = Source()
#     source_info: List[SourceInfo] = [SourceInfo()]
#     finding_info: FindingInfo = FindingInfo()


# source = Source(source_title="New Title", url="https://newexample.com", year_published=2023)
# source_info = SourceInfo(source_from=[source], highlights=["highlight1", "highlight2"])
# finding_info = FindingInfo(finding_title="New Finding", finding_insight="New insight", finding_info=[source_info])
# research_output = ResearchOutput(source=do_source, source_info=[do_source_info], finding_info=do_finding_info)
# topic_info = TopicInfo(topic_title="New Topic", topic_insights=["New Insight1", "New Insight2"], topic_info=[finding_info])    

