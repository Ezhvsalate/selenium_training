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


def add_duck_to_cart(driver, duck_type):
    """
    Поиск в блоке "Most Popular" уточки с определенным именем и добавление в корзину
    :param driver: объект webdriver
    :param duck_type: наименование добавляемой в корзину уточки :)
    """
    # Открываем главную страницу
    driver.get("http://localhost/2/en/")
    # Кликаем по уточке с заданным именем
    driver.find_element_by_css_selector('#box-most-popular ul.products li.product a[title="' + duck_type + '"]').click()
    # Получаем элемент - счетчик количества товаров в корзине
    quantity = driver.find_element_by_css_selector('#cart a.content span.quantity')
    # Нажимаем на кнопку добавления в корзину
    driver.find_element_by_name('add_cart_product').click()
    # Ждем, пока товар будет добавлен - значение счетчика увиличится на 1
    WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#cart a.content span.quantity'),
                                                                     str(int(
                                                                         quantity.get_attribute("textContent")) + 1)))


def remove_duck_from_cart(driver, ecpected_num_of_items):
    """
    Удаление уточки из корзины с проверкой обновления таблицы со списком заказов
    :param driver: объект webdriver
    :param ecpected_num_of_items: ожидаемое количество строк в таблице со списком заказов
    """
    # нажимаем на кнопку удаления из корзины
    driver.find_element_by_name('remove_cart_item').click()
    # ждем, пока количество строк в таблице со списком заказов станет равным ожидаемому
    WebDriverWait(driver, 10).until(
        lambda d: len(driver.find_elements_by_css_selector(
            '#order_confirmation-wrapper tr td:nth-of-type(4)')) == ecpected_num_of_items)


def test_remove_item_from_cart(driver):
    # устанавливаем неявное ожидание появления элемента в 1 секунду
    driver.implicitly_wait(1)
    # добавим в корзину трех разноцветных уточек
    add_duck_to_cart(driver, "Blue Duck")
    add_duck_to_cart(driver, "Green Duck")
    add_duck_to_cart(driver, "Red Duck")
    # переходим в корзину
    driver.find_element_by_css_selector('#cart a.link').click()
    # удаляем из корзины поочередно трех добавленных уточек
    for i in range(2, -1, -1):
        remove_duck_from_cart(driver, i)
