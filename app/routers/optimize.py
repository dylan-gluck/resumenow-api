from ..lib.agent import optimize_agent
from ..logger.logger import logger
from ..schema.resume import Resume
from ..schema.job import Job
from fastapi import APIRouter, HTTPException, Form
from agents import Runner

router = APIRouter()

@router.put("/optimize")
async def optimize_resume(resume: Resume = Form(...), job: Job = Form(...)):
    """
    Optimizes a resume based on the provided job description.

    Args:
        resume (Resume): JSON object representing the resume to be optimized.
        job (Job): The job description to be used for optimizing.

    Returns:
        status: HTTPStatus code
        data: JSON dictionary of optimized Resume info
    """

    try:
        resume = Resume.model_validate(resume)
        job = Job.model_validate(job)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    # LLMs love XML :)
    resume_xml = f"<resume>{resume.model_dump_json()}</resume>"
    job_xml = f"<job_description>{job.model_dump_json()}</job_description>"

    prompt = f"{resume_xml} {job_xml}"

    # Format extracted text to Job schema
    try:
        result = await Runner.run(optimize_agent, prompt)
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error processing resume with OpenAI API"
        )

    # Validate
    resume_data = result.final_output
    parsed_data = Resume.model_validate(resume_data)

    return {"status": 200, "data": {"resume": parsed_data}}
