import csv
import time

import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options

# Создаем объект опций для настройки браузера
options = Options()
options.add_argument("start-maximized")  # Запуск браузера в максимальном размере окна
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Исключаем детектирование автоматизации
options.add_experimental_option('useAutomationExtension', False)  # Отключаем расширение автоматизации

# Создаем список для хранения всех ссылок
all_link = []


def main():
    # Создаем экземпляр веб-драйвера Chrome с заданными опциями
    with webdriver.Chrome(options=options) as browser:
        # Настраиваем Stealth-режим для ухода от обнаружения ботов
        stealth(browser,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        page = 1
        while True:
            url = f'https://www.wildberries.ru/catalog/zhenshchinam/aksessuary/sumki-i-ryukzaki/ryukzaki?sort=popular&page={page}&fdlvr=120&fkind=1&f135736=135739'
            page += 1
            browser.get(url)
            time.sleep(3)

            # Получаем высоту страницы для прокрутки
            height = browser.execute_script("return document.body.scrollHeight")
            # Прокручиваем страницу с шагом 1000 пикселей
            for i in range(0, height + 200, 1000):
                browser.execute_script(f'window.scrollBy(0, {i})')
                time.sleep(3)

            len_before = len(all_link)  # Запоминаем количество ссылок до добавления новых
            # Добавляем найденные ссылки в список
            all_link.extend(
                [x.get_attribute('href') for x in browser.find_elements(By.CLASS_NAME, 'j-open-full-product-card')])

            # Проверяем, были ли добавлены новые ссылки
            if len(all_link) == len_before:
                break

            # Записываем найденные ссылки в CSV-файл
            with open('links.csv', 'w', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(['url'])
                for link in all_link:
                    writer.writerow([link])


if __name__ == '__main__':
    main()
