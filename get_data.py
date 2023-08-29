import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options

# Создаем объект опций для настройки браузера
options = Options()
options.add_argument("start-maximized")  # Запуск браузера в максимальном размере окна
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Исключаем детектирование автоматизации
options.add_experimental_option('useAutomationExtension', False)  # Отключаем расширение автоматизации

# Название файла CSV, в который будут записываться данные
TABLE_NAME = 'final.csv'


# Функция для создания таблицы с заголовками
def create_table(name, column_name):
    with open(name, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, delimiter=';', fieldnames=column_name)
        writer.writeheader()  # записываем заголовки в колонках


# Функция для записи данных в таблицу
def write_table(filename, dat):
    with open(filename, 'a', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, delimiter=';', fieldnames=list(dat))
        writer.writerow(dat)


def main():
    column_name = 'art', 'brand', 'price', 'name', 'value'
    create_table(TABLE_NAME, column_name)  # Создание таблицы с заголовками

    # Создаем экземпляр веб-драйвера Chrome с заданными опциями
    with webdriver.Chrome(options=options) as browser:
        # Открываем файл с ссылками
        with open('links.csv', 'r', encoding='utf-8-sig') as file:
            for link in csv.DictReader(file):
                try:
                    browser.get(link['url'])  # Переходим по URL
                    time.sleep(2)  # Даем странице время для загрузки

                    # Ожидаем появления элемента с ценой
                    WebDriverWait(browser, 4).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'price-block__final-price')))

                    # Раскрываем раздел с параметрами товара
                    browser.find_element(By.CLASS_NAME,
                                         'collapsible__toggle.j-parameters-btn.j-wba-card-item.j-wba-card-item-show').click()
                    time.sleep(1)

                    # Получаем данные о товаре
                    art = browser.find_element(By.CLASS_NAME, "product-article__copy").text
                    brand = browser.find_element(By.CLASS_NAME, "product-page__header").text
                    price = [x.text for x in browser.find_elements(By.CLASS_NAME, 'price-block__final-price')][1]
                    description_data = browser.find_elements(By.XPATH, '//tr[@class="product-params__row"]')

                    # Записываем данные о параметрах товара в таблицу
                    for data in description_data:
                        name = data.find_element(By.CSS_SELECTOR, 'th').text
                        value = data.find_element(By.CSS_SELECTOR, 'td').text
                        dat = {'art': art, 'brand': brand, 'price': price, 'name': name, 'value': value}
                        write_table(TABLE_NAME, dat)
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    main()
