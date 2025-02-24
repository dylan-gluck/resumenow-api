import os
from fastapi import APIRouter, Body, HTTPException
from google import genai
from vlmrun.hub.schemas.document.resume import Resume
from pydantic import BaseModel
from typing import Dict, Any

class FormatRequest(BaseModel):
    resume: Dict[str, Any]
    job_description: str

router = APIRouter()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


@router.put("/format")
async def format_resume(request: FormatRequest):
    """
    Formats a resume based on the provided job description.

    Args:
        request (FormatRequest): Contains resume data and job description
          - resume (dict): JSON object representing the resume to be formatted.
          - job_description (string): The job description to be used for formatting.

    Returns:
        status (HTTPStatus): The status of the formatting operation.
        data (Resume): The formatted resume object.
    """
    
    try:
        resume = Resume.model_validate(request.resume)
        job_description = request.job_description
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    # LLMs love XML :)
    resume_xml = f"<resume>{resume.model_dump_json()}</resume>"
    job_description_xml = f"<job_description>{job_description}</job_description>"

    prompt = "Refine the resume to best match the attached job description"
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config={
            "response_mime_type": "application/json",
            "response_schema": Resume,
        },
        contents=[
            resume_xml,
            job_description_xml,
            prompt,
        ],
    )

    parsed_data = Resume.model_validate(response.parsed)
    return {"status": 200, "data": parsed_data}
