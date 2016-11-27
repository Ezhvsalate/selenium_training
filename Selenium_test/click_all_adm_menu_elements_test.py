import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_click_all_adm_menu_elements(driver):
    # устанавливаем неявное ожидание появления элемента в 1 секунду
    driver.implicitly_wait(1)
    # входим в панель администратора
    driver.get("http://localhost/2/admin/login.php")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    # находим по CSS-селектору все пункты меню первого (верхнего) уровня
    menu_lvl_1_items = driver.find_elements_by_css_selector("ul#box-apps-menu li#app- a")
    # заносим ссылки на пункты меню верхнего уровня в список click_list,
    # т.к. после первого клика обращение к menu_lvl_1_items будет давать staleReferenceException
    click_list = []
    for lvl_1_item in menu_lvl_1_items:
        click_list.append(lvl_1_item.get_attribute("href"))
    # для каждого пункта меню верхнего уровня
    for link in click_list:
        # кликаем на пункт меню
        driver.find_element_by_css_selector('a[href="' + link + '"]').click()
        # проверяем наличие заголовка
        assert len(driver.find_elements_by_css_selector("h1")) == 1

        # ищем пункты 2 уровня для пункта с классом selected (появляются только после нажатия на родителя)
        menu_lvl_2_items = driver.find_elements_by_css_selector("ul#box-apps-menu li.selected ul.docs a")
        # если есть пункты 2 уровня(чтобы selenium не ждал каждый раз секунду, что они вдруг "появятся")
        if len(menu_lvl_2_items) > 0:
            # заполняем список ссылками на пункты
            lvl_2_click_list = []
            for lvl_2_item in menu_lvl_2_items:
                lvl_2_click_list.append(lvl_2_item.get_attribute("href"))
            # прокликиваем подпункты
            for link in lvl_2_click_list:
                driver.find_element_by_css_selector('a[href="' + link + '"]').click()
                # проверяем наличие заголовка
                assert len(driver.find_elements_by_css_selector("h1")) == 1
