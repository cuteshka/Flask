import requests

server_address = 'https://static-maps.yandex.ru/v1?'
api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'


def get_toponym(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return toponym


def get_city_map(city):
    toponym = get_toponym(city)
    params = {
        'apikey': api_key,
        'll': toponym['Point']['pos'].replace(' ', ','),
        'spn': '0.01,0.01'
    }

    response = requests.get(server_address, params)
    return response.content
