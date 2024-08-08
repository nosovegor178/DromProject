import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import json


def download_car_cards(car_cards, filename, folder):
    sanitized_filename = sanitize_filename(filename)
    path_to_file = os.path.join(folder, sanitized_filename)
    os.makedirs(folder, exist_ok=True)
    with open(path_to_file, 'w', encoding='utf8') as file:
        json.dump(car_cards, file, ensure_ascii=False)


# def download_image(filename, car_kind):
#     sanitized_filename = sanitize_filename(filename)
#     os.chdir(car_kind)
#     os.makedirs('media', exist_ok=True)
#     os.chdir(os.pardir)


def parse_car_cards(car_kind):
    parsed_cards = []
    url = f'https://spb.drom.ru/{car_kind}/all/'
    params = {
        'ph': 1,
        'unsold': 1,
        'mv': 0.7
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    car_cards = soup.find('div', class_='css-1nvf6xk ejck0o60').find_all('div', attrs={'data-ftid': 'bulls-list_bull'})
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
    return parsed_cards


if __name__ == '__main__':
    car_kinds = ['acura', 'baic', 'bmw', 'chevrolet', 'ford', 'honda']
    os.makedirs('cars', exist_ok=True)
    os.chdir('cars')
    for car_kind in car_kinds:
        parsed_cards = parse_car_cards(car_kind)
        print(len(parsed_cards))
        download_car_cards(parsed_cards, f'{car_kind}.json', car_kind)
