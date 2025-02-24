import json
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from vlmrun.hub.schemas.document.resume import Resume, ContactInfo, TechnicalSkills, Skill

client = TestClient(app)

@patch("app.routers.format.client")
def test_format_resume_success(mock_client):
    # Mock the LLM response
    mock_response = MagicMock()
    mock_response.parsed = {
        "contact_info": {
            "full_name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone": "555-123-4567"
        },
        "summary": "Experienced software engineer with a focus on AI applications",
        "education": [],
        "work_experience": [],
        "technical_skills": {
            "programming_languages": [
                {"name": "Python"},
                {"name": "TypeScript"}
            ],
            "frameworks_libraries": [
                {"name": "FastAPI"},
                {"name": "TensorFlow"}
            ]
        }
    }
    mock_client.models.generate_content.return_value = mock_response
    
    # Create test data
    resume_data = {
        "contact_info": {
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "123-456-7890"
        },
        "summary": "Software developer with 5 years experience",
        "education": [],
        "work_experience": [],
        "technical_skills": {
            "programming_languages": [
                {"name": "Python"},
                {"name": "JavaScript"}
            ],
            "frameworks_libraries": [
                {"name": "FastAPI"},
                {"name": "React"}
            ]
        }
    }
    
    job_description = "Looking for a software engineer with AI experience"
    
    # Make the request
    response = client.put(
        "/format",
        json={
            "resume": resume_data,
            "job_description": job_description
        }
    )
    
    # Verify response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == 200
    assert response_data["data"]["contact_info"]["full_name"] == "Jane Smith"
    assert "AI applications" in response_data["data"]["summary"]
    assert "TensorFlow" in [skill["name"] for skill in response_data["data"]["technical_skills"]["frameworks_libraries"]]
    
    # Verify LLM was called correctly
    mock_client.models.generate_content.assert_called_once()
    call_args = mock_client.models.generate_content.call_args[1]
    assert call_args["model"] == "gemini-2.0-flash"
    assert job_description in str(call_args["contents"])

@patch("app.routers.format.client")
def test_format_resume_invalid_input(mock_client):
    # Test with invalid input (missing required fields)
    response = client.put(
        "/format",
        json={
            "resume": {"invalid": "data"},
            "job_description": "Job description"
        }
    )
    
    # Verify response indicates validation error
    assert response.status_code == 422
    
    # Verify LLM was not called
    mock_client.models.generate_content.assert_not_called()