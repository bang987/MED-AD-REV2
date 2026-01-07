"""
Pytest configuration and fixtures.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    """Async HTTP client for testing."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture
def sample_review_request():
    """Sample review request data for testing."""
    return {
        "ad_id": "TEST-001",
        "ad_content": "최고의 의료 서비스를 제공합니다.",
        "platform": "naver_blog",
        "priority": "normal",
    }
