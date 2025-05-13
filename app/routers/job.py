from ..lib.httpx import fetch
from ..lib.agent import job_agent
from ..logger.logger import logger
from ..schema.job import Job
from fastapi import APIRouter, HTTPException, Form
from agents import Runner

router = APIRouter()

@router.put("/job")
async def job_info(url: str = Form(...)):
    """
    Fetch html from url using httpx
    Extract Job info from html using OpenAI Agents SDK
    Return Job info as JSON dictionary

    Args:
        url: String of the job posting from form data

    Returns:
        status: HTTPStatus code
        data: JSON dictionary of parsed Job info
    """

    # Fetch html from url using httpx
    html = await fetch(url)

    # Format extracted text to Job schema
    try:
        result = await Runner.run(job_agent, html)
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error processing job with OpenAI API"
        )

    # Validate
    job_data = result.final_output
    parsed_data = Job.model_validate(job_data)

    return {"status": 200, "data": {"job": parsed_data}}
