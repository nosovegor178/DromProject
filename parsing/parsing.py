import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import json


def download_file(data, filename, folder='json'):
    sanitized_filename = sanitize_filename(filename)
    path_to_file = os.path.join(folder, sanitized_filename)
    os.makedirs(folder, exist_ok=True)
    with open(path_to_file, 'wb') as file:
        json.dump(data, file)

def get_page_with_cars(car_kind):
    url = f'https://spb.drom.ru/{car_kind}/all/'
    params = {
        'ph': 1,
        'unsold': 1
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    car_cards = soup.find_all('div', attrs={'data-ftid': 'bulls-list_bull'})
    return car_cards

def parse_car_cards(car_cards):
    parsed_cards = []
    for car_card in car_cards:
        if car_card.find(
            'span', attrs={'data-ftid': 'bull_location'}
            ).text == 'Санкт-Петербург':
            parsed_cards.append(parse_car_card(car_card))
    return parsed_cards

def parse_car_card(car_card):
    parsed_card = {
        'price': car_card.find('span', class_="css-46itwz e162wx9x0").text
    }
    return parsed_card

def parse_all_car_kinds(car_kinds):
    for car_kind in car_kinds:
        parsed_cards = parse_car_cards(get_page_with_cars(car_kind))
        print(type(parsed_cards))
        download_file(parsed_cards, f'{car_kind}.json')

car_kinds = ['acura']
parse_all_car_kinds(car_kinds)
