from pydantic import BaseModel
from typing import Optional

class Education(BaseModel):
    degree: str
    institution: str
    year: str

class Certification(BaseModel):
    name: str
    institution: str
    year: str

class WorkExperience(BaseModel):
    title: str
    company: str
    start_date: str
    end_date: str
    description: str

class Project(BaseModel):
    title: str
    description: str
    link: str

class Resume(BaseModel):
    name: str
    email: str
    phone: str
    address: Optional[str] = None
    links: Optional[list[str]] = []
    skills: Optional[list[str]] = []
    work_experience: list[WorkExperience]
    projects: Optional[list[Project]] = []
    certifications: Optional[list[Certification]] = []
    education: Optional[list[Education]] = []
    languages: Optional[list[str]] = []
    interests: Optional[list[str]] = []
