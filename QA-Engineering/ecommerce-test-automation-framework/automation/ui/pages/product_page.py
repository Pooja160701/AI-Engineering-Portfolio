from ui.pages.base_page import BasePage

class ProductPage(BasePage):

    ADD_TO_CART_BUTTON = "#add-to-cart-sauce-labs-backpack"
    CART_ICON = ".shopping_cart_link"

    def add_item_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def go_to_cart(self):
        self.click(self.CART_ICON)