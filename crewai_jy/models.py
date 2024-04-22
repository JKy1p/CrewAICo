from typing import List, Union, Optional, Dict
from urllib.parse import quote
from pydantic import BaseModel, HttpUrl



# Represents a generic source of information with a formatted output
class Source(BaseModel):
    title: str
    url: HttpUrl
    year: Optional[int] = None

    def formatted_source(self) -> str:
        safe_url = quote(str(self.url), safe="/:[]@!$&'()*+,;=")
        return f"[{self.title}]({safe_url})" + (f", {self.year}" if self.year is not None else "")
    
# Holds detailed information with highlights and sources
class DetailedInfo(BaseModel):
    description: str
    metrics: Optional[Dict[str, Union[int, str, float]]] = None
    sources: List[Source]
    highlights: Optional[List[str]] = None

    # Method to add source information in the specified format
    def add_source_info(self):
        # Ensure URLs are appended correctly
        self.description += ' ' + ' '.join(source.formatted_source() for source in self.sources)

# Represents a subtopic with its detailed information
class SubTopic(BaseModel):
    name: str
    details: List[DetailedInfo]

# Top level model for a topic with its subtopics
class TopicInfo(BaseModel):
    title: str
    insights: List[str]
    subtopics: List[SubTopic]

# Topmost level model encapsulating all topics related to an account
class AccountInfo(BaseModel):
    account_name: str
    topics: List[TopicInfo]
    
    def generate_report(self) -> str:
        report = [f"Account: {self.account_name}\n"]
        
        for topic in self.topics:
            report.append(f"TopicInfo: {topic.title}\n{' '.join(f'Insight: {insight}' for insight in topic.insights)}")
            for subtopic in topic.subtopics:
                report.append(f"\nSubtopic: {subtopic.name}")
                report.extend(
                    f"Detail: {detail.description + ' '.join(source.formatted_source() for source in detail.sources)}"
                    for detail in subtopic.details
                )
        
        return "\n\n".join(report)






# Model for Referencing Information 
# class Source(BaseModel):
#     source_title: str = "Default Title"
#     url: Union[str, HttpUrl] = "http://example.com"
#     year_published: int = 2022

# # Next level up, incorporates Source with snippets
# class SourceInfo(BaseModel):
#     source_from: List[Source] 
#     highlights: List[str] = ["highlight1", "highlight2"]

# # More complex model, built from SourceInfo
# class FindingInfo(BaseModel):
#     finding_title: str = "Default Finding"
#     finding_insight: str = "Default insight"
#     finding_info: List[SourceInfo]

# # Top level model, built from FindingInfo
# class TopicInfo(BaseModel):
#     topic_title: str = "Topic"
#     topic_insights: List[str] = ["Insight1", "Insight2"]
#     topic_info: List[FindingInfo] 

# class AccountInfo(BaseModel):
#     account_name: str = "Target Account"
#     account_info: List[TopicInfo] 


# class ResearchOutput(BaseModel):
#     source: Source = Source()
#     source_info: List[SourceInfo] = [SourceInfo()]
#     finding_info: FindingInfo = FindingInfo()


# source = Source(source_title="New Title", url="https://newexample.com", year_published=2023)
# source_info = SourceInfo(source_from=[source], highlights=["highlight1", "highlight2"])
# finding_info = FindingInfo(finding_title="New Finding", finding_insight="New insight", finding_info=[source_info])
# research_output = ResearchOutput(source=do_source, source_info=[do_source_info], finding_info=do_finding_info)
# topic_info = TopicInfo(topic_title="New Topic", topic_insights=["New Insight1", "New Insight2"], topic_info=[finding_info])    

