from typing import Dict, List, Optional
from pydantic import BaseModel


class ContactInfo(BaseModel):
    full_name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]
    portfolio: Optional[str]
    google_scholar: Optional[str]


class Education(BaseModel):
    institution: Optional[str]
    degree: Optional[str]
    field_of_study: Optional[str]
    graduation_date: Optional[str]
    gpa: Optional[float]
    honors: Optional[List[str]]
    relevant_courses: Optional[List[str]]


class WorkExperience(BaseModel):
    company: Optional[str]
    position: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    is_current: bool
    responsibilities: List[str]
    technologies: Optional[List[str]]


class Skill(BaseModel):
    name: str
    level: Optional[str]
    years_of_experience: Optional[float]


class TechnicalSkills(BaseModel):
    programming_languages: List[Skill]
    frameworks_libraries: List[Skill]
    databases: Optional[List[Skill]]
    tools: Optional[List[Skill]]
    cloud_platforms: Optional[List[Skill]]
    other: Optional[List[Skill]]


class Project(BaseModel):
    name: str
    description: Optional[str]
    technologies: Optional[List[str]]
    url: Optional[str]
    github_url: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    role: Optional[str]
    key_achievements: Optional[List[str]]


class Certification(BaseModel):
    name: str
    issuer: str
    date_obtained: Optional[str]
    expiration_date: Optional[str]
    credential_id: Optional[str]


class OpenSourceContribution(BaseModel):
    project_name: str
    contribution_type: str
    description: str
    url: Optional[str]


class Resume(BaseModel):
    contact_info: ContactInfo
    summary: Optional[str]
    education: List[Education]
    work_experience: List[WorkExperience]
    technical_skills: TechnicalSkills
    projects: Optional[List[Project]]
    open_source_contributions: Optional[List[OpenSourceContribution]]
    certifications: Optional[List[Certification]]
    publications: Optional[List[str]]
    conferences: Optional[List[str]]
    languages: Optional[List[Skill]]
    volunteer_work: Optional[List[str]]
    interests: Optional[List[str]]
    references: Optional[str]
    additional_sections: Optional[Dict[str, List[str]]]
