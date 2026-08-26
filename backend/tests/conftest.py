import pytest
import asyncio
import os
from httpx import AsyncClient, ASGITransport
import pytest_asyncio

# Testing mode on karo
os.environ["TESTING"] = "true"

from main import app

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
        
        