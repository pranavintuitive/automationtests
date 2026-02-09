import pytest
from playwright.sync_api import sync_playwright

pytestmark = pytest.mark.ui
BASE_URL = "http://34.135.61.167:8000/"


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.mark.skip(reason="Known issue: bug #123")
def test_login(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{BASE_URL}/login")
    page.fill('input[name="username"]', "your_username")
    page.fill('input[name="password"]', "your_password")
    page.click('button[type="submit"]')
    page.wait_for_url(f"{BASE_URL}/dashboard")
    assert page.url == f"{BASE_URL}/dashboard"
    context.close()
