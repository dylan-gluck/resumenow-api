from io import BytesIO
from ..lib.agent import resume_agent
from ..logger.logger import logger
from ..schema.resume import Resume
from fastapi import APIRouter, UploadFile, File, HTTPException
from unstructured.partition.auto import partition
from agents import Runner

router = APIRouter()

@router.put("/parse")
async def parse_resume(file: UploadFile = File(...)):
    """
    Process resume document and return a dictionary of the parsed data.

    Args:
        file: File object (pdf, md, doc, docx)

    Returns:
        status: HTTPStatus code
        data: JSON dictionary of parsed Resume
    """
    supported_types = [
        "application/pdf",
        "application/doc",
        "text/markdown",
        "text/plain",
    ]

    if not file:
        logger.error("No file provided")
        raise HTTPException(status_code=422, detail="No file provided")

    if file.content_type not in supported_types:
        logger.error("Unsupported file type")
        raise HTTPException(status_code=422, detail="Unsupported file type")

    # Byte stream from UploadFile
    content = await file.read()
    content_stream = BytesIO(content)

    # Get text elements using unstructured
    elements = partition(file=content_stream)

    # Extract text from elements for JSON serialization
    text_elements = [str(element) for element in elements]

    # Stringify elements json for LLM
    string = "\n".join(text_elements)

    # Format extracted text to Resume schema
    try:
        result = await Runner.run(resume_agent, string)
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error processing resume with OpenAI API"
        )

    # Validate
    resume = result.final_output
    parsed_data = Resume.model_validate(resume)

    return {"status": 200, "data": {"resume": parsed_data}}
