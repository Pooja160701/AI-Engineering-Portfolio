import pytest
from ui.pages.login_page import LoginPage
from ui.pages.product_page import ProductPage

@pytest.mark.ui
@pytest.mark.regression
def test_add_item_to_cart(page):
    login_page = LoginPage(page)
    product_page = ProductPage(page)

    login_page.load()
    login_page.login("standard_user", "secret_sauce")

    product_page.add_item_to_cart()
    product_page.go_to_cart()

    assert "cart" in page.url