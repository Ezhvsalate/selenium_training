from selenium import webdriver
from pages.main_page import MainPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


class Application:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(1)

        self.main_page = MainPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)

    def quit(self):
        self.driver.quit()

    def add_several_products_to_cart(self, valid_list_of_products):
        for product_name in valid_list_of_products.product_names:
            self.main_page.open()
            self.main_page.open_popular_product_by_name(product_name)
            self.product_page.add_product_to_cart()

    def remove_objects_from_cart_one_by_one(self):
        self.cart_page.open()
        for i in range(0, self.cart_page.count_objects_in_cart()):
            self.cart_page.remove_element_from_cart()
