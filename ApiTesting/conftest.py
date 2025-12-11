import pytest
from playwright.sync_api import sync_playwright
from api_client import APIClient

BASE_URL = "http://192.168.1.202:8080"


@pytest.fixture(scope="session")
def token():
    client = APIClient(BASE_URL)
    t = client.login("superadmin", "Admin@1234")
    print("\n🔑 Logged in once.\n")
    return t


@pytest.fixture(scope="session")
def request_context(token):
    with sync_playwright() as p:
        ctx = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )
        yield ctx
