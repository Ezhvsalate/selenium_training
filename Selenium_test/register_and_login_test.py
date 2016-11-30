import pytest
from selenium import webdriver
from random import randint


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_register_and_login(driver):
    #   генерируем рандомное число, будет использовано для создания уникального адреса почты
    usernum = str(randint(100000,999999))
    # устанавливаем неявное ожидание появления элемента в 5 секунд
    driver.implicitly_wait(5)
    # переходим на форму регистрации
    driver.get("http://localhost/2/en/create_account")
    # заполняем необходимые поля
    driver.find_element_by_name("firstname").send_keys("Login")
    driver.find_element_by_name("lastname").send_keys("Loginov")
    driver.find_element_by_name("address1").send_keys("High road, 1")
    driver.find_element_by_name("postcode").send_keys("410000")
    driver.find_element_by_name("city").send_keys("Sin city")
    driver.find_element_by_name("email").send_keys("user"+usernum+"@yandex.ru")
    driver.find_element_by_name("phone").send_keys("123456")
    driver.find_element_by_name("password").send_keys("pass1word$")
    driver.find_element_by_name("confirmed_password").send_keys("pass1word$")
    driver.find_element_by_name("create_account").click()
    # выходим из созданного аккаунта
    driver.find_element_by_css_selector('#box-account ul.list-vertical li:nth-of-type(4) a').click()
    # снова входим
    driver.find_element_by_name("email").send_keys("user"+usernum+"@yandex.ru")
    driver.find_element_by_name("password").send_keys("pass1word$")
    driver.find_element_by_name("login").click()
    # и выходим
    driver.find_element_by_css_selector('#box-account ul.list-vertical li:nth-of-type(4) a').click()