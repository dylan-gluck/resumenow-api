import io
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@patch("app.routers.parse.client")
def test_parse_resume_pdf_success(mock_client):
    # Mock the LLM response
    mock_response = MagicMock()
    mock_response.parsed = {
        "contact_info": {
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "123-456-7890",
        },
        "summary": "Experienced software engineer",
        "education": [],
        "work_experience": [],
        "technical_skills": {
            "programming_languages": [{"name": "Python"}, {"name": "Java"}],
            "frameworks_libraries": [{"name": "FastAPI"}, {"name": "Spring Boot"}],
        },
    }
    mock_client.models.generate_content.return_value = mock_response

    # Create a mock PDF file
    test_file = io.BytesIO(b"%PDF-1.5 mock pdf content")

    # Make the request
    response = client.put(
        "/parse", files={"file": ("resume.pdf", test_file, "application/pdf")}
    )

    # Verify response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == 200
    assert response_data["data"]["contact_info"]["full_name"] == "John Doe"
    assert "Experienced software engineer" in response_data["data"]["summary"]
    assert "Python" in [
        skill["name"]
        for skill in response_data["data"]["technical_skills"]["programming_languages"]
    ]

    # Verify LLM was called correctly
    mock_client.models.generate_content.assert_called_once()
    call_args = mock_client.models.generate_content.call_args[1]
    assert call_args["model"] == "gemini-2.0-flash"
    assert "Extract all available resume information" in str(call_args["contents"])


@patch("app.routers.parse.client")
def test_parse_resume_text_success(mock_client):
    # Mock the LLM response
    mock_response = MagicMock()
    mock_response.parsed = {
        "contact_info": {
            "full_name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone": "555-123-4567",
        },
        "summary": "Senior developer with 10 years experience",
        "education": [],
        "work_experience": [],
        "technical_skills": {
            "programming_languages": [{"name": "Java"}],
            "frameworks_libraries": [{"name": "Spring"}],
        },
    }
    mock_client.models.generate_content.return_value = mock_response

    # Create a mock text file
    test_file = io.BytesIO(
        b"Jane Smith\nSenior Developer\nSkills: Java, Spring, Kubernetes"
    )

    # Make the request
    response = client.put(
        "/parse", files={"file": ("resume.txt", test_file, "text/plain")}
    )

    # Verify response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == 200
    assert response_data["data"]["contact_info"]["full_name"] == "Jane Smith"
    assert "Senior developer" in response_data["data"]["summary"]
    assert "Java" in [
        skill["name"]
        for skill in response_data["data"]["technical_skills"]["programming_languages"]
    ]


@patch("app.routers.parse.client")
def test_parse_resume_markdown_success(mock_client):
    # Mock the LLM response
    mock_response = MagicMock()
    mock_response.parsed = {
        "contact_info": {
            "full_name": "Alex Johnson",
            "email": "alex.johnson@example.com",
            "phone": "777-888-9999",
        },
        "summary": "Full-stack developer specializing in web applications",
        "education": [],
        "work_experience": [],
        "technical_skills": {
            "programming_languages": [{"name": "JavaScript"}],
            "frameworks_libraries": [{"name": "React"}, {"name": "Node.js"}],
        },
    }
    mock_client.models.generate_content.return_value = mock_response

    # Create a mock markdown file
    test_file = io.BytesIO(
        b"# Alex Johnson\n\n## Skills\n- React\n- Node.js\n- MongoDB"
    )

    # Make the request
    response = client.put(
        "/parse", files={"file": ("resume.md", test_file, "text/markdown")}
    )

    # Verify response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == 200
    assert response_data["data"]["contact_info"]["full_name"] == "Alex Johnson"
    assert "web applications" in response_data["data"]["summary"]
    assert "React" in [
        skill["name"]
        for skill in response_data["data"]["technical_skills"]["frameworks_libraries"]
    ]


def test_parse_resume_unsupported_file_type():
    # Create a mock HTML file
    test_file = io.BytesIO(b"<html><body>Resume content</body></html>")

    # Make the request
    response = client.put(
        "/parse", files={"file": ("resume.html", test_file, "text/html")}
    )

    # Verify response indicates validation error
    assert response.status_code == 422
    assert "Unsupported file type" in response.json()["detail"]
