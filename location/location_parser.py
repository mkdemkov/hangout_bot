import os
import math
import foursquare
import requests


def parse_location(latitude, longitude, radius):
    url = 'https://api.foursquare.com/v3/places/search'

    params = {
        'query': 'coffee',
        # 'client_id': os.getenv('CLIENT_ID'),
        # 'client_secret': os.getenv('CLIENT_SECRET'),
        'll': f'{latitude},{longitude}',
        'open_now': 'true',
        'radius': radius,
        'sort': 'DISTANCE'
        # 'categoryId': '4d4b7105d754a06374d81259,4bf58dd8d48988d16d941735,4bf58dd8d48988d116941735',
        # 'v': '20220424'
    }

    token = os.getenv('API_KEY')

    headers = {
        'Accept': 'application/json',
        'Authorization': f'{token}'
    }

    response = requests.request('GET', url, params=params, headers=headers).json()

    with open('static/response.json', 'w') as file:
        file.write(str(response))

    nearby_venues = []
    for venue in response['results']:
        name = venue['name']
        category = venue['categories'][0]['name']
        # price = venue.get('price', {}).get('tier')
        address = venue['location']['address']
        distance = venue['distance']
        nearby_venues.append({'name': name, 'category': category, 'address': address, 'distance': distance})

    return nearby_venues

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
