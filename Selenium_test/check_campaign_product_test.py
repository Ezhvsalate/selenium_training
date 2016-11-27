import pytest
from selenium import webdriver

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_check_campaign_product(driver):
    # устанавливаем неявное ожидание появления элемента в 1 секунду
    driver.implicitly_wait(1)
    # открываем страницу
    driver.get("http://localhost/2")
    # получаем список продуктов в блоке campaigns
    campaign_products = driver.find_elements_by_css_selector("#box-campaigns li.product")
    # получаем наименование продукта, старую и акционную цены
    text = campaign_products[0].find_element_by_css_selector("div.name").text
    old_price = campaign_products[0].find_element_by_css_selector("div.price-wrapper s.regular-price").get_attribute("textContent")
    newPrice = campaign_products[0].find_element_by_css_selector("div.price-wrapper strong.campaign-price").get_attribute("textContent")
    # переходим на страницу продукта
    campaign_products[0].click()
    # получаем наименование продукта, старую и акционную цены на странице продукта
    p_text = driver.find_element_by_css_selector("h1.title").text
    p_old_price = driver.find_element_by_css_selector("#box-product div.price-wrapper s.regular-price").get_attribute("textContent")
    p_new_price = driver.find_element_by_css_selector("#box-product div.price-wrapper strong.campaign-price").get_attribute("textContent")
    # проверяем, что наименование и цены в блоке campaigns и на странице продукта совпадают
    assert(text==p_text and old_price==p_old_price and newPrice==p_new_price)

    # можно было бы сделать проверку стилей, получив цвет-размер каждой цены, например, так:
    # old_price_color = campaign_products[0].find_element_by_css_selector("div.price-wrapper s.regular-price").value_of_css_property("color")
    # и затем сравнить с ожидаемым значением rgba(119, 119, 119, 1)
    # но я этого делать не буду, т.к. исходя из материалов лекции код получится не кросс-браузерный и проверить то, что
    # первая цена серая, зачёркнутая, маленькая, вторая цена красная жирная, крупная - правильнее вручную