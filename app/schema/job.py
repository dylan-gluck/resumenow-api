from typing import List, Optional
from pydantic import BaseModel


class Job(BaseModel):
    company: str
    title: str
    description: str
    salary: Optional[str]
    responsibilities: Optional[List[str]]
    qualifications: Optional[List[str]]
    logistics: Optional[List[str]]
    location: Optional[List[str]]
    additional_info: Optional[List[str]]
    link: Optional[str]
