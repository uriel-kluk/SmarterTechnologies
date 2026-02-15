import os
from fastapi import Header, HTTPException
from typing import Callable


def get_test_token() -> str:
    return os.getenv("API_TEST_TOKEN", "test-token")


def require_auth(authorization: str | None = Header(None)) -> None:
    """Minimal auth dependency: validates bearer token only."""
    token = get_test_token()
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    provided = authorization.split(" ", 1)[1]
    if provided != token:
        raise HTTPException(status_code=403, detail="Forbidden")


def require_role(role: str) -> Callable:
    """Return a dependency that enforces a role present in the `X-Roles` header.

    Header `X-Roles` should be a comma-separated list of roles. This is a
    minimal RBAC placeholder for tests/MVP. In production this would read
    role claims from a validated JWT.
    """

    def _checker(authorization: str | None = Header(None), x_roles: str | None = Header(None)) -> None:
        # First validate token
        require_auth(authorization)
        if x_roles is None:
            raise HTTPException(status_code=403, detail="Forbidden: missing roles")
        roles = [r.strip() for r in x_roles.split(",") if r.strip()]
        if role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden: insufficient role")

    return _checker
