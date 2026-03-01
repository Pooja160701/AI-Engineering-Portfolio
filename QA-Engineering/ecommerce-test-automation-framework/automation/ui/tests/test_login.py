import pytest
from ui.pages.login_page import LoginPage

@pytest.mark.ui
@pytest.mark.smoke
def test_valid_login(page):
    login_page = LoginPage(page)

    login_page.load()
    login_page.login("standard_user", "secret_sauce")

    assert "inventory" in page.url

@pytest.mark.ui
@pytest.mark.regression
def test_invalid_login(page):
    login_page = LoginPage(page)

    login_page.load()
    login_page.login("invalid_user", "wrong_password")

    assert "Epic sadface" in login_page.get_error_message()