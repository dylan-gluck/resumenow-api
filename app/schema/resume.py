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
    institution: str
    degree: str
    field_of_study: Optional[str]
    graduation_date: Optional[str]
    gpa: Optional[float]
    honors: List[str]
    relevant_courses: List[str]


class WorkExperience(BaseModel):
    company: str
    position: str
    start_date: Optional[str]
    end_date: Optional[str]
    is_current: Optional[bool]
    responsibilities: List[str]
    technologies: List[str]


class Skill(BaseModel):
    name: str
    level: Optional[str]
    years_of_experience: Optional[float]


class TechnicalSkills(BaseModel):
    programming_languages: List[Skill]
    frameworks_libraries: List[Skill]
    databases: List[Skill]
    tools: List[Skill]
    cloud_platforms: List[Skill]
    other: List[Skill]


class Project(BaseModel):
    name: str
    description: Optional[str]
    technologies: List[str]
    url: Optional[str]
    github_url: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    role: Optional[str]
    key_achievements: List[str]


class Certification(BaseModel):
    name: str
    issuer: str
    date_obtained: Optional[str]
    expiration_date: Optional[str]
    credential_id: Optional[str]


class OpenSourceContribution(BaseModel):
    project_name: str
    contribution_type: Optional[str]
    description: Optional[str]
    url: Optional[str]


class Resume(BaseModel):
    contact_info: ContactInfo
    summary: Optional[str]
    education: List[Education]
    work_experience: List[WorkExperience]
    technical_skills: TechnicalSkills
    projects: List[Project]
    open_source_contributions: List[OpenSourceContribution]
    certifications: List[Certification]
    publications: List[str]
    conferences: List[str]
    languages: List[Skill]
    volunteer_work: List[str]
    interests: List[str]
    references: List[str]
    additional_sections: Optional[Dict[str, List[str]]]
