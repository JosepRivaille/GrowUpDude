from flask import Flask, request, abort, jsonify
from geopy.geocoders import Nominatim
import json
import urllib.request

app = Flask(__name__)


def calculate_route(cities):
    return json.dumps(cities, ensure_ascii=False)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/params')
def get_parameters_list():
    parameters = {
        'economy': 'numeric',
        'daysRange': 'range/days',
    }
    return jsonify(**parameters)


@app.route('/cities')
def get_all_cities():
    city_name = request.args.get('city_name', None)
    if city_name is None:
        abort(400)
    try:
        if city_name is None:
            raise ValueError('Unexisting data')
        radius = float(request.args.get('radius', 0))
    except ValueError:
        abort(400)

    country = None
    with open('./webapp/resources/json/countriesToCities.json') as file:
        """
        country_city_json = json.load(file)
        for json_country in country_city_json:
            for json_city in country_city_json[json_country]:
                if json_city == city_name:
                    country = json_country
        """
        # TODO: Translate to english name format
        APIKEY = "AIzaSyCae5qjNTc_T1LFkfjyjqfyfsIlZbuEMn8"
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + city_name + "&key=" + APIKEY
        country_city_json = urllib.request.urlopen(url).read()
        country_city = country_city_json['results']
        _, country = country_city.split(',')
        country = country[1:]

        near_cities = country_city_json[country]
        file.close()

    geo_locator = Nominatim()
    location = geo_locator.geocode(city_name)

    for city in near_cities:
        new_loc = geo_locator.geocode(city)
        if not new_loc.latitude - location.latitude < radius or not new_loc.longitude - location.longitude < radius:
            near_cities.remove(city)

    calculate_route(near_cities)


if __name__ == '__main__':
    app.run()