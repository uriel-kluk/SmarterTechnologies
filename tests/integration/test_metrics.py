import pytest
from httpx import AsyncClient
from src.api import app


@pytest.mark.asyncio
async def test_metrics_exposes_request_counters():
    """Acceptance:
    - After at least one `/sort` call the `/metrics` endpoint should expose request counters
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = {"Authorization": "Bearer test-token", "X-Roles": "sort:invoke"}
        await ac.post("/sort", json={"width": 10, "height": 10, "length": 10, "mass": 5}, headers=headers)
        r = await ac.get("/metrics")
        assert r.status_code == 200
        text = r.text
        # check our metric name
        assert "app_http_requests_total" in text
