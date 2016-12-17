from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class ProductPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def add_product_to_cart(self):
        quantity = self.driver.find_element_by_css_selector('#cart a.content span.quantity')
        self.driver.find_element_by_name('add_cart_product').click()
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#cart a.content span.quantity'),
                                             str(int(
                                                 quantity.get_attribute("textContent")) + 1)))