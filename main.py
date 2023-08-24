import csv
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium_stealth import stealth
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as ES
options = Options()
# ua = UserAgent()
# user_agent = ua.random
# options.add_argument(f"'User-agent'={user_agent}")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
all_data = []

with webdriver.Chrome(options=options) as browser:
    stealth(browser,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    browser.get('https://www.wildberries.ru/catalog/zhenshchinam/aksessuary/sumki-i-ryukzaki/ryukzaki#c147526479')
    time.sleep(3)
    height = browser.execute_script("return document.body.scrollHeight")
    with open('res.csv', 'a', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Наименование', 'Ключевые теги', 'Цена', 'Характеристики'])

        for i in range(0,height+200,1000):
            browser.execute_script(f'window.scrollBy(0,{i})')
            time.sleep(3)
        all_link = [x.get_attribute('href') for x in browser.find_elements(By.CLASS_NAME, 'j-open-full-product-card')]
        for link in all_link[:1]:
            browser.get(link)
            time.sleep(1)
            WebDriverWait(browser,4).until(EC.presence_of_element_located((By.CLASS_NAME,'price-block__final-price')))
            tags = browser.find_element(By.CSS_SELECTOR, 'h1').text
            brand = browser.find_element(By.CLASS_NAME, "product-page__header").text
            price = [x.text for x in browser.find_elements(By.CLASS_NAME, 'price-block__final-price')]
            # description =[x.find_element(By.TAG_NAME,'span').text for x in browser.find_elements(By.CLASS_NAME, 'product-params__cell')]
            browser.find_element(By.CLASS_NAME, 'collapsible__toggle.j-parameters-btn.j-wba-card-item.j-wba-card-item-show').click()
            try:
                description_name = [x.text for x in browser.find_elements(By.XPATH, '//span[@class="product-params__cell-decor"]/span') if x]
                description_value = [x.text for x in browser.find_elements(By.XPATH, '//td[@class="product-params__cell"]/span') if x]
            except Exception as e:
                print(e)
            browser.back()
            time.sleep(2)
            flatten = brand,tags, price[1], [x for x in zip(description_name, description_value)]
            writer = csv.writer(file, delimiter=';')
            writer.writerow(flatten)















    # try:
    #     captcha = browser.find_element_by_name("CaptchaInputText")
    #     captcha.click()
    # except:
    #     pass
    # # находим и кликаем 'Каталог'
    # browser.get('https://www.ozon.ru/')
    # time.sleep(5)
    # browser.find_element(By.CLASS_NAME, 'a2-a4').click()
    # try:
    #     captcha = browser.find_element_by_name("CaptchaInputText")
    #     captcha.click()
    # except:
    #     pass
    # time.sleep(10)
    # # browser.execute_script("window.scrollBy(0,5000)")
    # # button = browser.find_element(By.CSS_SELECTOR, '.a2-a button.a2-a4')
    # # button.click()
    # # time.sleep(10)


