from fastapi import APIRouter
from ..types import Resume

router = APIRouter()

@router.put("/format")
async def format_resume(resume: Resume, job_description: str):
    """
    Formats a resume based on the provided job description.

    Args:
        resume (Resume): The resume to be formatted.
        job_description (str): The job description to be used for formatting.

    Returns:
        dict: The formatted resume.
    """
    formatted_resume = {
        "name": "",
        "email": "",
        "phone": "",
        "address": "",
        "links": [],
        "skills": [],
        "work_experience": [],
        "projects": [],
        "certifications": [],
        "education": [],
        "languages": [],
        "interests": []
    }
    return formatted_resume
