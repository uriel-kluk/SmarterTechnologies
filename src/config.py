import os


def get_env(key: str, default: str | None = None) -> str | None:
    return os.getenv(key, default)


def get_api_test_token() -> str:
    return get_env("API_TEST_TOKEN", "test-token")
