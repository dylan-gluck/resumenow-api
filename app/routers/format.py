import os
from fastapi import APIRouter
from google import genai
from vlmrun.hub.schemas.document.resume import Resume

router = APIRouter()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


@router.put("/format")
async def format_resume(resume: Resume, job_description: str):
    """
    Formats a resume based on the provided job description.

    Args:
        resume (Resume): JSON object representing the resume to be formatted.
        job_description (string): The job description to be used for formatting.

    Returns:
        status (HTTPStatus): The status of the formatting operation.
        data (Resume): The formatted resume object.
    """

    # LLMs love XML :)
    resume_xml = f"<resume>{resume.json()}</resume>"
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
