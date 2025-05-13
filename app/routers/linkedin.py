from ..lib.httpx import fetch
from ..lib.agent import resume_agent
from ..logger.logger import logger
from ..schema.resume import Resume
from fastapi import APIRouter, HTTPException, Form
from agents import Runner

router = APIRouter()

@router.put("/linkedin")
async def linkedin_resume(url: str = Form(...)):
    """
    Fetch html from url using httpx
    Extract Resume info from html using OpenAI API
    Return Resume info as JSON dictionary

    Args:
        url: String of the linkedin profile

    Returns:
        status: HTTPStatus code
        data: JSON dictionary of parsed Resume info
    """

    # Fetch html from url using httpx
    html = await fetch(url)

    # Format extracted text to Job schema
    try:
        result = await Runner.run(resume_agent, html)
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error processing resume with OpenAI API"
        )

    # Validate
    resume_data = result.final_output
    parsed_data = Resume.model_validate(resume_data)

    return {"status": 200, "data": {"resume": parsed_data}}
