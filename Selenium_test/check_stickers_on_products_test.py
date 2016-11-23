import pytest
from selenium import webdriver

@pytest.fixture
def driver(request):
    wd = webdriver.Firefox(firefox_binary="c:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe")
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_click_all_adm_menu_elements(driver):
    driver.get("http://localhost/2/")
    elements_list = driver.find_elements_by_css_selector("li.product.column")
    for element in elements_list:
        assert len(element.find_elements_by_css_selector("div.sticker"))==1

