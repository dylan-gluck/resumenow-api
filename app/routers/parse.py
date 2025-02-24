import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from google import genai
from google.genai import types
from vlmrun.hub.schemas.document.resume import Resume

router = APIRouter()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


@router.put("/parse")
async def parse_resume(file: UploadFile = File(...)):
    """
    Process resume document and return a dictionary of the parsed data.

    Args:
        file: File object (pdf, md, txt)

    Returns:
        status: HTTPStatus code
        data: JSON dictionary of parsed Resume
    """

    if file.content_type == "application/pdf":
        pass
    elif file.content_type == "text/markdown":
        pass
    elif file.content_type == "text/plain":
        pass
    else:
        raise HTTPException(status_code=422, detail="Unsupported file type")

    content = await file.read()

    prompt = "Extract all available resume information"
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config={
            "response_mime_type": "application/json",
            "response_schema": Resume,
        },
        contents=[
            types.Part.from_bytes(
                data=content,
                mime_type=file.content_type,
            ),
            prompt,
        ],
    )

    parsed_data = Resume.model_validate(response.parsed)
    return {"status": 200, "data": parsed_data}
