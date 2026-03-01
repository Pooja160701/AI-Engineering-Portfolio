import pytest
from playwright.sync_api import sync_playwright
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.fixture(scope="session")
def browser():
    logger.info("Launching browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=Config.HEADLESS)
        yield browser
        browser.close()
        logger.info("Browser closed.")

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(Config.TIMEOUT)
    page.set_default_navigation_timeout(Config.TIMEOUT)
    yield page
    context.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page", None)
        if page:
            page.screenshot(path=f"reports/{item.name}.png")