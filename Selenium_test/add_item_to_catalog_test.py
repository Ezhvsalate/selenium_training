import pytest
from selenium import webdriver
from random import randint


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_add_item_to_catalog(driver):
    #   генерируем рандомное число, будет использовано для создания уникального адреса почты
    product_num = str(randint(100000,999999))

    # устанавливаем неявное ожидание появления элемента в 5 секунд
    driver.implicitly_wait(5)

    # входим в панель администратора
    driver.get("http://localhost/2/admin/login.php")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    driver.get("http://localhost/2/en/create_account")

    # переходим на страницу добавления товара
    driver.get("http://localhost/2/admin/?app=catalog&doc=catalog")

    # Нажимаем на кнопку "Add new product"
    driver.find_element_by_css_selector('td#content a.button:nth-of-type(2)').click()
    # Заполняем поля на вкладке  "General"
    driver.find_element_by_name("name[en]").send_keys(product_num)
    driver.find_element_by_name("code").send_keys(product_num)
    driver.find_element_by_name("quantity").send_keys(1)
    driver.find_element_by_name("date_valid_from").send_keys("01.12.2016")
    driver.find_element_by_name("date_valid_to").send_keys("31.12.2016")
    # Переходим на вкладку "Informaion" и заполняем поля на ней
    driver.find_element_by_css_selector('div.tabs ul.index li:nth-of-type(2)').click()
    manufact_selector = driver.find_element_by_css_selector('#tab-information select[name="manufacturer_id"]')
    manufact_selector.click()
    manufact_selector.find_element_by_css_selector('option[value="1"]').click()
    driver.find_element_by_name("short_description[en]").send_keys(product_num)
    driver.find_element_by_name("description[en]").send_keys(product_num)
    driver.find_element_by_name("head_title[en]").send_keys(product_num)
    driver.find_element_by_name("meta_description[en]").send_keys(product_num)
    # Переходим на вкладку "Prices" и заполняем поля на ней
    driver.find_element_by_css_selector('div.tabs ul.index li:nth-of-type(4)').click()
    driver.find_element_by_name("purchase_price").send_keys(1)
    currency_selector = driver.find_element_by_css_selector('#tab-prices select[name="purchase_price_currency_code"]')
    currency_selector.click()
    currency_selector.find_element_by_css_selector('option[value="USD"]').click()
    driver.find_element_by_name("prices[USD]").send_keys(2)
    # Нажимаем на кнопку "Save"
    driver.find_element_by_css_selector('span.button-set button[name="save"]').click()
    # Получаем список наименований продуктов
    products_data = driver.find_elements_by_css_selector("table.dataTable tr.row td:nth-of-type(3)")
    product_names_list = []
    for product in products_data:
        product_names_list.append(product.text)
    # Проверяем, что наш продукт входит в список
    assert(str(product_num) in product_names_list)
