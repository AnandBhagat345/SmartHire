import pytest
import uuid

def unique_email():
    return f"test_{uuid.uuid4().hex[:8]}@gmail.com"

# Helper — login karke token lo
async def get_token(client):
    email = unique_email()
    await client.post("/auth/register", json={
        "name": "Job Test User",
        "email": email,
        "password": "test123"
    })
    response = await client.post("/auth/login", data={
        "username": email,
        "password": "test123"
    })
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_create_job(client):
    token = await get_token(client)
    response = await client.post("/jobs/", 
        json={
            "company_name": "Google",
            "job_role": "Backend Developer",
            "status": "Applied"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_get_jobs(client):
    token = await get_token(client)
    response = await client.get("/jobs/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_job(client):
    token = await get_token(client)
    # Pehle job banao
    create = await client.post("/jobs/",
        json={
            "company_name": "Amazon",
            "job_role": "DevOps",
            "status": "Applied"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    job_id = create.json()["id"]
    
    # Update karo
    response = await client.put(f"/jobs/{job_id}",
        json={"status": "Interview Scheduled"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_job(client):
    token = await get_token(client)
    # Pehle job banao
    create = await client.post("/jobs/",
        json={
            "company_name": "Microsoft",
            "job_role": "SDE",
            "status": "Applied"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    job_id = create.json()["id"]
    
    # Delete karo
    response = await client.delete(f"/jobs/{job_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_unauthorized_access(client):
    response = await client.get("/jobs/")
    assert response.status_code == 401