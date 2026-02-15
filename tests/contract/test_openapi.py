import pytest
from src.api import app


def test_openapi_contains_sort():
    """Acceptance:
    - OpenAPI schema must include POST /sort with a response containing property `stack`.
    """
    schema = app.openapi()
    assert "/sort" in schema.get("paths", {}), "Missing /sort path in OpenAPI schema"
    post_op = schema["paths"]["/sort"].get("post")
    assert post_op is not None
    # Check responses for 200 and that the schema defines `stack`
    responses = post_op.get("responses", {})
    ok = responses.get("200") or responses.get("201")
    assert ok is not None, "No 200/201 response defined for /sort"
    # Drill into JSON schema if present (may vary by implementation)
    content = ok.get("content", {})
    app_json = content.get("application/json", {})
    schema_obj = app_json.get("schema", {})
    # Best-effort check for 'stack' property in schema
    props = schema_obj.get("properties") or {}
    assert "stack" in props, "Response model missing 'stack' property"
