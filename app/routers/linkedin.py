import os
import httpx
from ..logger.logger import logger
from ..schema.resume import Resume
from fastapi import APIRouter, HTTPException, Form
from openai import OpenAI

router = APIRouter()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


async def fetch_html(url: str) -> str:
    """
    Fetch html from url using httpx

    Args:
        url: String of the url to scrape

    Returns:
        html: String of the html content
    """
    try:
        response = httpx.get(url)
        return response.text
    except Exception as e:
        logger.error(f"Failed to fetch html from {url}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch html")


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

    logger.info(f"Fetching html from {url}")

    # Fetch html from url using httpx
    html = await fetch_html(url)

    # Format extracted text to Job schema
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Extract the Resume information."},
                {"role": "user", "content": html},
            ],
            response_format=Resume,
        )
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error processing resume with OpenAI API"
        )

    # Validate
    resume_data = completion.choices[0].message.parsed
    parsed_data = Resume.model_validate(resume_data)

    return {"status": 200, "data": {"resume": parsed_data}}
