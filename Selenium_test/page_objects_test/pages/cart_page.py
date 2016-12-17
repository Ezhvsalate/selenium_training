from selenium.webdriver.support.wait import WebDriverWait


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("http://localhost/2/en/checkout")
        return self

    def remove_element_from_cart(self):
        expected_number_of_items = self.count_objects_in_cart() - 1
        self.driver.find_element_by_name('remove_cart_item').click()
        WebDriverWait(self.driver, 10).until(
            lambda d: self.count_objects_in_cart() == expected_number_of_items)

    def count_objects_in_cart(self):
        return int(len(self.driver.find_elements_by_css_selector(
            '#order_confirmation-wrapper tr td:nth-of-type(4)')))
