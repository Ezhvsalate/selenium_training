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


def find_window_other_than(driver, old_windows):
    new_windows = driver.window_handles
    for window in new_windows:
        if window not in old_windows:
            return window

def test_check_external_links(driver):
    # устанавливаем неявное ожидание появления элемента в 5 секунд
    driver.implicitly_wait(5)
    # входим в панель администратора
    driver.get("http://localhost/2/admin/login.php")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    # переходим на страницу со списком стран
    driver.get("http://localhost/2/admin/?app=countries&doc=countries")
    # нажимаем кнопку добавления новой страны
    driver.find_element_by_css_selector('td#content a.button').click()

    # запоминаем текущее окно и открытые окна
    main_window = driver.current_window_handle
    old_windows = driver.window_handles
    # находим внешние ссылки
    external_links = driver.find_elements_by_css_selector('i.fa-external-link')
    # кликаем по каждой из найденных внешних ссылок, ждем пока откроется новое окно, активируем его,
    #  закрываем и возвращаемся в главное окно
    for link in external_links:
        link.click()
        WebDriverWait(driver, 10).until(EC.new_window_is_opened(old_windows))
        driver.switch_to_window(find_window_other_than(driver, old_windows))
        driver.close()
        driver.switch_to_window(main_window)