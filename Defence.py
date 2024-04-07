from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd
import os
from Parsing_RIA import urls, setup_chrome_driver, save_base, Path

def get_cards_from_deepmind(driver, url, category):
    try:
        driver.get(url)

        for i in range(200000):
            if i % 100 == 0:
                if save_base(driver = driver, category= category, i= i):
                    break

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(0.01)

            try:
                if i <= 5:
                    more_button = driver.find_element(By.CLASS_NAME, 'list-more')
                    more_button.click()
                    sleep(0.1)

            except Exception as e:
                pass

        driver.quit()  
        
    except Exception as e:
                pass

if __name__ == "__main__":
    download_folder = os.getcwd()
    for category in urls.keys():
        for url in urls[category]:
            print(category, url)
            driver = setup_chrome_driver(download_folder)
            get_cards_from_deepmind(driver, url, category)
