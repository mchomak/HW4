from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from Parsing_RIA import urls, setup_chrome_driver, save_base, Path, thems


def get_info_from_cards(card_urls, id):
    data = {
        "url": [],
        "headers": [],
        "sub_headers": [],
        "text": [],
        "ID": []
    }

    for idx, url in enumerate(card_urls):
        try:
            response = requests.get(url)
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
        
            try:
                data['headers'].append(soup.find('h1', class_='article__title').text)
            except Exception as e:
                try:
                    data['headers'].append(soup.find('div', class_='article__title').text)
                except Exception as e:
                    data['headers'].append(None)

            try:
                data['sub_headers'].append(soup.find('h1', class_='article__second-title').text)
            except Exception as e:
                data['sub_headers'].append(None)

            try:
                data['text'].append(' '.join([p.text for p in soup.find_all('div', class_='article__text')]))
            except Exception as e:
                data['text'].append(None)
            
            data['ID'].append(id)
            data['url'].append(url)

            if idx % 1000 == 0:
                print(idx, url)
        
        except Exception as e:
            pass

    
    return pd.DataFrame(data)


if __name__ == "__main__":
    for key in Path.keys():
        files = os.listdir(Path[key])
        print(files)
        for file in files:
            print(os.path.join(Path[key], file))
            df = pd.read_csv(os.path.join(Path[key], file))
            card_urls = df["URL"].tolist()
            info_df = get_info_from_cards(card_urls, thems[key])
            
            save_path = os.path.join('data', f'{thems[key]}_info.csv')
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            info_df.to_csv(save_path, index=False)