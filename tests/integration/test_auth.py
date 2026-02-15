import pytest
from httpx import AsyncClient
from src.api import app


@pytest.mark.asyncio
async def test_sort_requires_auth():
    """Acceptance:
    - Unauthenticated requests to `POST /sort` SHOULD return 401
    - Requests with a valid token SHOULD return 200 and payload {"stack": ...}
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # unauthenticated
        r = await ac.post("/sort", json={"width": 10, "height": 10, "length": 10, "mass": 5})
        assert r.status_code == 401

        # authenticated with known test token but missing role -> forbidden
        headers = {"Authorization": "Bearer test-token"}
        r3 = await ac.post("/sort", json={"width": 10, "height": 10, "length": 10, "mass": 5}, headers=headers)
        assert r3.status_code == 403

        # authenticated with token and required role
        headers = {"Authorization": "Bearer test-token", "X-Roles": "sort:invoke"}
        r2 = await ac.post("/sort", json={"width": 10, "height": 10, "length": 10, "mass": 5}, headers=headers)
        assert r2.status_code == 200
        assert r2.json() == {"stack": "STANDARD"}
