import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_check_countries_order(driver):
    # устанавливаем неявное ожидание появления элемента в 1 секунду
    driver.implicitly_wait(1)
    # входим в панель администратора
    driver.get("http://localhost/2/admin/login.php")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    # переходим на страницу со списком стран
    driver.get("http://localhost/2/admin/?app=countries&doc=countries")

    # для каждой строки таблицы определяем наименование страны и добавляем в список countries_list
    countries_data = driver.find_elements_by_css_selector("table.dataTable tr.row")
    countries_list = []
    urls_to_check_zones = []
    for country in countries_data:
        # использовать :nth-of-type(х) не очень хорошо, но в данном случае не знаю, как иначе
        country_name = country.find_element_by_css_selector("td:nth-of-type(5)")
        countries_list.append(country_name.text)
        # для каждой строки таблицы определяем количество зон, если оно больше 0 - добавляем в список
        # urls_to_check_zones адреса, по которым проверим сортировку зон
        num_of_zones = country.find_element_by_css_selector("td:nth-of-type(6)").text
        if int(num_of_zones) > 0:
            urls_to_check_zones.append(
                country.find_element_by_css_selector("td:nth-of-type(5) a").get_attribute("href"))
    # проверяем, что страны отсортированы в правильном порядке
    assert countries_list == sorted(countries_list)
    # переходим по каждому урлу из списка urls_to_check_zones
    for url in urls_to_check_zones:
        driver.get(url)
        zones_list = []
        # получаем названия зон по CSS-селектору и добавляем в список zones_list
        zones_data = driver.find_elements_by_css_selector(
            'table#table-zones tr:not(.header) td:nth-of-type(3) input[type=hidden]')
        for zone in zones_data:
            zones_list.append(zone.get_attribute("value"))
        # проверяем, что получившийся список зон отсортирован
        assert zones_list == sorted(zones_list)

def test_check_geo_zones_order(driver):
    # устанавливаем неявное ожидание появления элемента в 1 секунду
    driver.implicitly_wait(1)
    # входим в панель администратора
    driver.get("http://localhost/2/admin/login.php")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    # переходим на страницу со списком геозон
    driver.get("http://localhost/2/admin/?app=geo_zones&doc=geo_zones")
    # для каждой строки таблицы добавляем URL по которому нужно проверить сортировку зон в список urls_to_check_zones
    countries_data = driver.find_elements_by_css_selector("table.dataTable tr.row td:nth-of-type(3) a")
    urls_to_check_zones = []
    for country in countries_data:
        urls_to_check_zones.append(country.get_attribute("href"))
    # переходим по каждому урлу из списка urls_to_check_zones
    for url in urls_to_check_zones:
        driver.get(url)
        zones_list = []
        # получаем названия зон по CSS-селектору и добавляем в список zones_list
        zones_data = driver.find_elements_by_css_selector(
            'table#table-zones tr:not(.header) td select[name*=zone_code] option[selected=selected]')
        for zone in zones_data:
            zones_list.append(zone.text)
        # проверяем, что получившийся список зон отсортирован
        assert zones_list == sorted(zones_list)
