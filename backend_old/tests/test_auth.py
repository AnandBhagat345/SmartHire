import pytest
import uuid

def unique_email():
    return f"test_{uuid.uuid4().hex[:8]}@gmail.com"

@pytest.mark.asyncio
async def test_register_success(client):
    response = await client.post("/auth/register", json={
        "name": "Test User",
        "email": unique_email(),
        "password": "test123"
    })
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    email = unique_email()
    await client.post("/auth/register", json={
        "name": "Test User",
        "email": email,
        "password": "test123"
    })
    response = await client.post("/auth/register", json={
        "name": "Test User",
        "email": email,
        "password": "test123"
    })
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_login_success(client):
    email = unique_email()
    await client.post("/auth/register", json={
        "name": "Login Test",
        "email": email,
        "password": "test123"
    })
    response = await client.post("/auth/login", data={
        "username": email,
        "password": "test123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_wrong_password(client):
    email = unique_email()
    await client.post("/auth/register", json={
        "name": "Test User",
        "email": email,
        "password": "test123"
    })
    response = await client.post("/auth/login", data={
        "username": email,
        "password": "wrongpassword"
    })
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_user_not_found(client):
    response = await client.post("/auth/login", data={
        "username": f"notexist_{uuid.uuid4().hex}@gmail.com",
        "password": "test123"
    })
    assert response.status_code == 404