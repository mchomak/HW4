import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from tqdm import tqdm
import time
import os

main_path = os.getcwd()

Path = {
        # 'Общество/Россия' : os.path.join(main_path, "data", "Social"),
        # 'Экономика' : os.path.join(main_path, "data", "Economy"),
        # 'Силовые структуры' : os.path.join(main_path, "data", "Defence"),
        # 'Бывший СССР' : os.path.join(main_path, "data", "CCCR"),
        'Спорт' : os.path.join(main_path, "data", "Sport"),
        # 'Забота о себе' : os.path.join(main_path, "data", "Health"),
        # 'Строительство' : os.path.join(main_path, "data", "Build"),
        # 'Туризм/Путешествия' : os.path.join(main_path, "data", "Tourism"),
        # 'Наука и техника' : os.path.join(main_path, "data", "Since")
        }

thems = {'Общество/Россия' : 0,
        'Экономика' : 1,
        'Силовые структуры' : 2,
        'Бывший СССР' : 3,
        'Спорт' : 4,
        'Забота о себе' : 5,
        'Строительство' : 6,
        'Туризм/Путешествия' : 7,
        'Наука и техника' : 8
        }

urls = {
        'Общество/Россия' : ["https://ria.ru/society/"],
        'Экономика' : ["https://ria.ru/economy/"],
        'Силовые структуры' : ["https://ria.ru/defense_safety/"],
        'Бывший СССР' : [],
        'Спорт' : [
            "https://rsport.ria.ru/football/",
            "https://rsport.ria.ru/hockey/",
            "https://rsport.ria.ru/figure_skating/",
            "https://rsport.ria.ru/tennis/",
            "https://rsport.ria.ru/fights/",
            "https://rsport.ria.ru/lyzhnye-gonki/",
            "https://rsport.ria.ru/biathlon/",
            "https://rsport.ria.ru/category_formula_1/",
            "https://rsport.ria.ru/zozh/"
                    ],
        'Забота о себе' : ["https://ria.ru/sn_health/"],
        'Строительство' : [],
        'Туризм/Путешествия' : [
                                "https://ria.ru/tourism_navigator/",
                                "https://ria.ru/tourism_visual/",
                                "https://ria.ru/tourism_food/",
                                "https://ria.ru/category_intervyu_turizm/",
                                "https://ria.ru/tourism_news/"
                                ],
        'Наука и техника' : ["https://ria.ru/science/"]
        }


def setup_chrome_driver(download_folder):
    """
    Настраивает драйвер Chrome с указанными опциями.
    
    :param download_folder: Папка для загрузки файлов.
    :return: Инициализированный драйвер.
    """
    chrome_options = Options()
    prefs = {"download.default_directory": download_folder}
    chrome_options.add_experimental_option("prefs", prefs)
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def save_base(driver, category, i):
        cards_elements = driver.find_elements(By.CSS_SELECTOR, 'a.list-item__title.color-font-hover-only')
        cards_urls = [element.get_attribute('href') for element in cards_elements]
        print(f"[INFO] Cards count is {len(cards_urls)}")

        df = pd.DataFrame(cards_urls, columns=['URL'])

        df.to_csv(os.path.join(Path[category], f"{i}_{len(cards_urls)}.csv"), index=False)
        return len(cards_urls) >= 3000




def get_cards_from_deepmind(url):
    cards_urls = []
    try:
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        cards = soup.find_all('a', class_='list-item__title color-font-hover-only')
        print(f"[INFO] Cards count is {len(cards)}")
        for card in cards:
            card_url=card["href"]
            cards_urls.append(card_url)
        
        return cards_urls
            
    except (AttributeError, TypeError) as ex:
        print(f"[ERROR] {ex}")
        return cards_urls


def get_cards_from_synced(url):
    cards_urls = []
    try:
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        cards = soup.find_all('h2', class_='entry-title')
        print(f"[INFO] Cards count is {len(cards)}")
        for card in cards:
            card_url=card.find("a")["href"]
            cards_urls.append(card_url)
        
        return cards_urls
            
    except (AttributeError, TypeError) as ex:
        print(f"[ERROR] {ex}")
        return cards_urls


def save_data(urls):
    df=pd.DataFrame({
                      "card_link":urls
                      })
    df.to_csv('cards_urls_page_1.csv', index= False )


def get_cards_from_urls(urls):
    cards_urls = []
    for url in urls.keys():
        cards_urls += urls[url](url)
    
    return cards_urls


def main():
    # url = urls['Общество/Россия']
    # print(url)
    # cards_urls = get_cards_from_deepmind(url = url)
    # print(len(cards_urls))
    # save_data(cards_urls)
    # print(f"[INFO] DataBase sucsefully saved")
    pass


if __name__=="__main__":
    main()