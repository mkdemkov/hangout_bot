import json
import logging
import os
import math
from asyncio import sleep

import aiohttp
import foursquare
import requests


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


def count_distance(long1, lat1, long2, lat2):
    R = 6371000  # radius of the Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(long2 - long1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


async def parse_location(latitude, longitude, radius):
    logging.basicConfig(level=logging.INFO)
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

    # async with aiohttp.ClientSession() as session:
    #     async with session.get(
    #             f'https://search-maps.yandex.ru/v1/?apikey=76ba2dbd-dc7c-4d4b-99e9-eeb0c55329ab&text=бар&ll={longitude},{latitude}&type=biz&results=10&lang=ru_RU') as resp:
    #         response_json = json.loads(await resp.text())
    #         with open('static/response.json', 'w') as file:
    #             file.write(str(response_json))
    #         features = response_json['features']
    #         nearby_bars = []
    #         for feature in features:
    #             distance = feature['properties']['Distance']
    #             if distance <= 1500:
    #                 nearby_bars.append(feature)
    #         return nearby_bars

    # url = 'https://api.foursquare.com/v3/places/search'
    #
    # params = {
    #     # 'query': 'Coffe',
    #     'categories': 13003,
    #     # 'client_id': os.getenv('CLIENT_ID'),
    #     # 'client_secret': os.getenv('CLIENT_SECRET'),
    #     'll': f'{latitude},{longitude}',
    #     'open_now': 'true',
    #     'price' : 1,
    #     'radius': radius,
    #     'sort': 'DISTANCE',
    #     'limit' : 5
    #     # 'categoryId': '4d4b7105d754a06374d81259,4bf58dd8d48988d16d941735,4bf58dd8d48988d116941735',
    #     # 'v': '20220424'
    # }
    #
    # token = os.getenv('API_KEY')
    #
    # headers = {
    #     'Accept': 'application/json',
    #     'Authorization': f'{token}'
    # }
    #
    # response = requests.request('GET', url, params=params, headers=headers).json()
    # # response = requests.get(url, headers=headers)
    #
    # with open('static/response.json', 'w') as file:
    #     file.write(str(response))
    #
    # nearby_venues = []
    # for venue in response['results']:
    #     name = venue['name']
    #     category = venue['categories'][0]['name']
    #     # price = venue.get('price', {}).get('tier')
    #     address = venue['location']['address']
    #     distance = venue['distance']
    #     nearby_venues.append({'name': name, 'category': category, 'address': address, 'distance': distance})
    #
    # return nearby_venues

    # location = Location(longitude=longitude, latitude=latitude)
    #
    # headers = {
    #     'Accept': 'application/json',
    #     'Authorization': os.getenv('API_KEY')
    # }
    #
    # # Make a request to the Foursquare API to search for bars near your location
    # url = 'https://api.foursquare.com/v3/places/search'
    # params = {
    #     'client_id': os.getenv('CLIENT_ID'),
    #     'client_secret': os.getenv('CLIENT_SECRET'),
    #     'll': f"{location.latitude},{location.longitude}",
    #     'query': type_of_location,
    #     'radius': 1500,
    #     'price': price,
    #     'v': str(datetime.today().strftime('%Y%m%d'))  # today's date
    # }
    # response = requests.get(url, params=params, headers=headers).json()
    #
    # # Parse the response to extract the names of the bars that are within 500 meters of your location and that are free
    # bars = {}
    # with open('static/response.json', 'w') as file:
    #     file.write(str(response))
    # for venue in response['response']['venues']:
    #     if venue['location']['distance'] <= 2000 and venue['price']['tier'] == 0:
    #         name = venue['name']
    #         bars[name]['distance'] = venue['location']['distance']
    #         bars[name]['price'] = venue['price']
    #
    # # Return the list of bar names
    # return bars
    # gmaps = googlemaps.Client(key=os.getenv('API_KEY'))
    # location = (latitude, longitude)  # current location
    # radius = 1500  # maximum distance for places
    # language = 'ru'
    #
    # places = gmaps.places_nearby(
    #     location=location,
    #     radius=radius,
    #     keyword=type_of_location,
    #     language=language,
    #     open_now=True,
    #     type=type_of_location
    # )
    #
    # return places
