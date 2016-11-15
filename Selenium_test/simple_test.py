import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Firefox(firefox_binary="c:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe")
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("http://yandex.ru/")
    driver.find_element_by_name("text").send_keys("Санкт-Петербург")
    driver.find_element_by_class_name("button_theme_websearch").click()
    WebDriverWait(driver, 10).until(EC.title_contains("Санкт-Петербург"))