import pytest
import uuid
from io import BytesIO
from reportlab.pdfgen import canvas

def unique_email():
    return f"resume_{uuid.uuid4().hex[:8]}@gmail.com"


#  token generate
async def get_token(client):
    email = unique_email()

    await client.post(
        "/auth/register",
        json={
            "name": "Resume Test User",
            "email": email,
            "password": "test123"
        }
    )

    response = await client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "test123"
        }
    )

    return response.json()["access_token"]


# Fake PDF file
def fake_pdf():

    buffer = BytesIO()

    p = canvas.Canvas(buffer)

    p.drawString(100, 750, "This is a test resume")
    p.drawString(100, 730, "Python Django REST API")

    p.save()

    buffer.seek(0)

    return buffer


# Test analyse Resume

@pytest.mark.asyncio
async def test_analyze_resume(client):

    token = await get_token(client)

    response = await client.post(
        "/resume/analyze",
        files={
            "file": (
                "resume.pdf",
                fake_pdf(),
                "application/pdf"
            )
        },
        data={
            "job_description":
            "Looking for Python developer with Django and REST API skills"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    # status check
    assert response.status_code in [200, 500]

    # AI success case
    if response.status_code == 200:
        data = response.json()

        assert "ats_score" in data
        assert "missing_keywords" in data
        assert "suggestions" in data



# Test History

@pytest.mark.asyncio
async def test_resume_history(client):

    token = await get_token(client)

    response = await client.get(
        "/resume/history",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)



# Test Rewrite Resume

@pytest.mark.asyncio
async def test_resume_rewrite(client):

    token = await get_token(client)

    response = await client.post(
        "/resume/rewrite",
        json={
            "resume_text":
            "Built a Django project with authentication and APIs.",

            "job_description":
            "Looking for Python Backend Developer with Django REST APIs"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in [200, 500]

    if response.status_code == 200:
        data = response.json()

        assert "rewritten_text" in data
        assert isinstance(data["rewritten_text"], str)


# Test Unauthorized Access
@pytest.mark.asyncio
async def test_resume_unauthorized(client):

    response = await client.get("/resume/history")

    assert response.status_code == 401