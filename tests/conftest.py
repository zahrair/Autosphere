import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "http://172.24.67.254:8080/#/"

@pytest.fixture(scope="session")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        print(f"\n🌐 Opening site: {BASE_URL}")
        page.goto(BASE_URL)
        yield page
        context.close()
        browser.close()
