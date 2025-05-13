import httpx
from ..logger.logger import logger
from fastapi import HTTPException

async def fetch(url: str) -> str:
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
