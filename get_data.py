import csv
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
all_link = []

TABLE_NAME = 'final.csv'
def create_table(name, column_name):
    with open(name, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, delimiter=';', fieldnames=column_name).writeheader() # записываем заголовки в колонках


def write_table(filename, dat):
    with open(filename, 'a', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file,delimiter=';', fieldnames=list(dat)).writerow(dat)

def main():
    column_name = ['art', 'brand', 'price', 'name', 'value']
    create_table(TABLE_NAME, column_name)
    with webdriver.Chrome(options=options) as browser:
        with open('links.csv', 'r', encoding='utf-8-sig') as file:
            for link in csv.DictReader(file):
                try:
                    browser.get(link['url'])
                    time.sleep(2)
                    WebDriverWait(browser, 4).until(EC.presence_of_element_located((By.CLASS_NAME, 'price-block__final-price')))
                    browser.find_element(By.CLASS_NAME,
                                         'collapsible__toggle.j-parameters-btn.j-wba-card-item.j-wba-card-item-show').click()
                    time.sleep(1)

                    art = browser.find_element(By.CLASS_NAME, "product-article__copy").text
                    brand = browser.find_element(By.CLASS_NAME, "product-page__header").text
                    price = [x.text for x in browser.find_elements(By.CLASS_NAME, 'price-block__final-price')]
                    description_data = browser.find_elements(By.XPATH, '//tr[@class="product-params__row"]')
                    for data in description_data:
                        name = [x.text for x in data.find_elements(By.CSS_SELECTOR, 'th')]
                        value = [x.text for x in data.find_elements(By.CSS_SELECTOR, 'td')]
                        dat = {'art': art, 'brand': brand, 'price': price, 'name': name, 'value': value}
                        write_table(TABLE_NAME, dat)
                except Exception as e:
                    print(e)









if __name__ == '__main__':
    main()