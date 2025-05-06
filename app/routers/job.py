import os
import httpx
from ..logger.logger import logger
from ..schema.job import Job
from fastapi import APIRouter, HTTPException
from openai import OpenAI

router = APIRouter()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


async def fetch_html(url: str) -> str:
    """
    Fetch html from url using httpx

    Args:
        url: String of the job posting

    Returns:
        html: String of the html content
    """
    try:
        response = httpx.get(url)
        return response.text
    except Exception as e:
        logger.error(f"Failed to fetch html from {url}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch html")


@router.put("/job")
async def job_info(url: str):
    """
    Fetch html from url using httpx
    Extract Job info from html using OpenAI API
    Return Job info as JSON dictionary

    Args:
        url: String of the job posting

    Returns:
        status: HTTPStatus code
        data: JSON dictionary of parsed Job info
    """

    logger.info(f"Fetching html from {url}")

    # Fetch html from url using httpx
    html = await fetch_html(url)

    # Format extracted text to Job schema
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Extract the Job information."},
                {"role": "user", "content": html},
            ],
            response_format=Job,
        )
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error processing job with OpenAI API"
        )

    # Validate
    job_data = completion.choices[0].message.parsed
    parsed_data = Job.model_validate(job_data)

    return {"status": 200, "data": {"job": parsed_data}}
