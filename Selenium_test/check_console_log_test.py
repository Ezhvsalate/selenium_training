import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_check_console_log(driver):
    # устанавливаем неявное ожидание появления элемента в 5 секунд
    driver.implicitly_wait(5)
    # входим в панель администратора
    driver.get("http://localhost/2/admin/login.php")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    # переходим на страницу со списком продуктов
    driver.get("http://localhost/2/admin/?app=catalog&doc=catalog&category_id=1")

    # находим ссылки на редактирование продуктов
    product_links = driver.find_elements_by_css_selector(
        'table.dataTable tr.row td:nth-of-type(3) a[href*=edit_product]')
    urls_to_check_log = []
    # собираем ссылки в список
    for product in product_links:
        urls_to_check_log.append(product.get_attribute("href"))

    # проходим по каждой ссылке и проверяем отсутствие вхождения строк 'error' и 'warning' в логах браузера
    for url in urls_to_check_log:
        driver.get(url)
        for l in driver.get_log("browser"):
            assert "error" not in l
            assert "warning" not in l
