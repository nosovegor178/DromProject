import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from itertools import count
import json


def download_car_cards(car_cards, filename, folder):
    sanitized_filename = sanitize_filename(filename)
    path_to_file = os.path.join(folder, sanitized_filename)
    os.makedirs(folder, exist_ok=True)
    with open(path_to_file, 'w', encoding='utf8') as file:
        json.dump(car_cards, file, ensure_ascii=False)


def download_image(car_kind, filename, image_url):
    sanitized_filename = sanitize_filename(filename)
    os.makedirs(car_kind, exist_ok=True)
    os.chdir(car_kind)
    os.makedirs('media', exist_ok=True)
    path_to_file = os.path.join('media', sanitized_filename)
    response = requests.get(image_url)
    response.raise_for_status()
    with open(path_to_file, 'wb') as file:
        file.write(response.content)
    os.chdir(os.pardir)


def parse_car_cards(car_kind):
    parsed_cards = []
    image_urls = []
    params = {
        'ph': 1,
        'unsold': 1,
        'mv': 0.7
    }
    for page_number in count(1):
        url = f'https://spb.drom.ru/{car_kind}/all/page{page_number}'
        response = requests.get(url, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        if not soup.find('div', attrs={'data-bulletin-list': 'true'}):
            break
        else:
            car_cards = soup.find('div', attrs={'data-bulletin-list': 'true'}).find_all('div', attrs={'data-ftid': 'bulls-list_bull'})
            for car_card in car_cards:
                title = car_card.find('h3', class_='css-16kqa8y efwtv890').text.split(',')
                auto_info = car_card.find('div', class_='css-1fe6w6s e162wx9x0').text.split(',')
                engine_power_info = auto_info[0].split('(')
                parsed_card = {
                        'model': title[0],
                        'year': title[1],
                        'price': car_card.find('span', class_="css-46itwz e162wx9x0").text,
                        'horsepower': engine_power_info[1][:-1],
                        'engine_info': f'{engine_power_info[0]}, {auto_info[1]}',
                        'transmission': auto_info[2],
                        'drive': auto_info[3],
                        }
                try:
                    parsed_card['mileage'] = auto_info[4]
                except IndexError:
                    print('Без пробега')
                parsed_cards.append(parsed_card)
                image_urls.append(car_card.find('div', attrs={'data-ftid': 'bull_image'}).find(
                    'div', attrs={'data-first-photo': 'true'}).find(
                    'div', class_='css-aqyz46 e1e9ee560').find('img')['src'])
    return parsed_cards, image_urls


if __name__ == '__main__':
    car_kinds = ['acura', 'baic', 'citroen', 'belgee', 'porsche', 'jaguar']
    os.makedirs('cars', exist_ok=True)
    os.chdir('cars')
    for car_kind in car_kinds:
        parsed_cards = parse_car_cards(car_kind)[0]
        download_car_cards(parsed_cards, f'{car_kind}.json', car_kind)
        for image_number, image_url in enumerate(parse_car_cards(car_kind)[1]):
            download_image(car_kind, f'{car_kind}_{image_number+1}.png', image_url)