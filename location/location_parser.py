import logging
import os
import math
from asyncio import sleep
import requests


# Function to get rating and price of the given place
def get_rating_and_price(id):
    logging.basicConfig(level=logging.INFO)
    url = 'https://api-maps.yandex.ru/2.1/'
    api_key = os.getenv('YANDEX')
    params = {
        'apikey': api_key,
        'id': id,
        'lang': 'ru_RU',
        'type': 'biz'
    }
    try:
        response = requests.get(url, params=params)
        response_json = response.text
        print(response_json)
    except:
        logging.info(f'Ошибка при выполнение запроса: {response}')


# Function to count distance in metres between to places
def count_distance(long1, lat1, long2, lat2):
    R = 6371000  # radius of the Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(long2 - long1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


# Function to find nearby places according to its type and budget
async def parse_location(latitude, longitude, type, budget):
    logging.basicConfig(level=logging.INFO)
    type = str(type)[2:-3]
    budget = str(budget)[2:-3]
    url = 'https://search-maps.yandex.ru/v1/'
    api_key = os.getenv('YANDEX')
    params = {
        'apikey': api_key,
        'text': 'кафе',
        'll': f'{longitude},{latitude}',
        'spn': f'{0.1},{0.1}',
        'type': 'biz',
        'results': 50,
        'lang': 'ru_RU',
        'rspn': 1
    }

    response = requests.get(url, params=params).json()

    with open('static/response.json', 'w') as file:
        file.write(str(response))

    places = {}
    counter = 0

    # parce every location
    for feature in response['features']:
        places[counter] = {}
        place = feature['properties']
        info = place['CompanyMetaData']
        id = info['id']
        long = place['boundedBy'][0][0]
        lat = place['boundedBy'][0][1]
        distance = count_distance(longitude, latitude, long, lat)
        places[counter]['distance'] = distance
        if (int(distance) <= 1500):
            get_rating_and_price(id)
            await sleep(0.8)
        try:
            name = info['name']
            address = info['address']
            try:
                phone = info['Phones'][0]['formatted']
            except:
                phone = 'Отсутствует'
            places[counter]['name'] = name
            places[counter]['address'] = address
            places[counter]['phone'] = phone
        except Exception:
            logging.info('Что-то пошло не так при попытке распарсить какое-то поле')
        counter += 1

    return places
