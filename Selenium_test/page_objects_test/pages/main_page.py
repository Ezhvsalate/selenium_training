from selenium.webdriver.support.wait import WebDriverWait


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("http://localhost/2/en/")
        return self

    def open_popular_product_by_name(self, product_name):
        self.driver.find_element_by_css_selector(
            '#box-most-popular ul.products li.product a[title="' + product_name + '"]').click()
