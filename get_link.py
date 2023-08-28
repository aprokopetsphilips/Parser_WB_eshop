import csv
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
all_link = []

def main():
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
        for i in range(0,height+200,1000):
            browser.execute_script(f'window.scrollBy(0,{i})')
            time.sleep(3)
        all_link.extend([x.get_attribute('href') for x in browser.find_elements(By.CLASS_NAME, 'j-open-full-product-card')])

        with open('links.csv', 'w', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['url'])
            for link in all_link:
                writer.writerow([link])

if __name__ == '__main__':
    main()


