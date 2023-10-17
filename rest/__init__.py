#!/usr/bin/env python
import os
import json
from datetime import datetime
from http import HTTPStatus
from flask import Flask
from flask import render_template
from flask import request
from flask import Response
import requests

from rest.databases.shoes import get_products, get_product_by_id

# create the application object
app = Flask(__name__)

OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY', '')


def dict_to_json_response(data, status):
    response = Response(response=json.dumps(data).encode('utf-8'),
                        status=status,
                        content_type='application/json')
    return response


# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('welcome.html')  # render a template


#
# Returns all products in the catalog
#
@app.route('/products', methods=['GET'])
def search_for_orders():
    app.logger.debug(f"Content-Type: {request.content_type}")
    app.logger.debug(f"Args: {type(request.args)}")
    response = dict_to_json_response({"products": get_products()}, status=HTTPStatus.OK)
    return response


#
# Returns a product from the catalog by its product id using HTTP GET
#
@app.route('/products/item/<product_id>', methods=['GET'])
def get_order(product_id):
    response = None
    app.logger.debug(request.headers)
    if request.headers['accept'] != 'application/json':
        response = dict_to_json_response({"result": "Incorrect accept header"}, HTTPStatus.METHOD_NOT_ALLOWED)
    elif product_id is None:
        response = dict_to_json_response({"result": "Product Id Missing"}, HTTPStatus.BAD_REQUEST)
    elif get_product_by_id(product_id) is not None:
        product = get_product_by_id(product_id)
        response = dict_to_json_response({"products": [product]}, HTTPStatus.OK)
    else:
        response = dict_to_json_response({"result": "Product Not Found"}, HTTPStatus.NOT_FOUND)
    return response


#
# Returns a product from the catalog by its product id using HTTP POST
#
@app.route('/products', methods=['POST'])
def lookup_order():
    response = None
    if request.data is None:
        response = dict_to_json_response({"request": "Product id not specified"}, HTTPStatus.BAD_REQUEST)
    elif request.headers['accept'] != 'application/json':
        response = dict_to_json_response({"result": "Incorrect accept header"}, HTTPStatus.METHOD_NOT_ALLOWED)
    elif request.content_type != 'application/json':
        response = dict_to_json_response({"result": "Incorrect content-type header"}, HTTPStatus.BAD_REQUEST)
    else:
        app.logger.debug(f"data: {request.get_json()}")
        doc = json.loads(request.data.decode('utf-8'))
        product_id = doc['product_id']
        if 'product_id' in doc:
            product = get_product_by_id(product_id)
            response = dict_to_json_response({"products": [product]}, HTTPStatus.OK)
        else:
            response = dict_to_json_response({"request": "Product id not specified"},
                                             HTTPStatus.BAD_REQUEST)
    return response


@app.route('/nlx/action-proxy', methods=['POST'])
def action_proxy():
    doc = request.get_json()
    app.logger.debug(doc)

    return dict_to_json_response({}, HTTPStatus.OK)


@app.route('/nlx/rest-proxy', methods=['POST'])
def rest_proxy():
    doc = request.get_json()
    app.logger.debug(json.dumps(doc))
    url = "https://httpbin.org/post"

    payload = {}
    headers = {
        'accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    app.logger.debug(response.text)
    data = {
        "resolvedVariables": [
            {
                "variableId": "RPRestCall",
                "value": {
                    "status": str(response.status_code),
                    "body": str(response.text)
                }
            }
        ],
        "unresolvedVariables": [],
        "context": {}
    }
    data['context']['body'] = response.text
    data['context']['status'] = str(response.status_code)
    app.logger.debug(f'data: {json.dumps(data, sort_keys=True, indent=4)}')
    return dict_to_json_response(data, HTTPStatus.OK)


@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    # TODO: Implement the checks as an exception
    # if OPEN_WEATHER_API_KEY is None:
    #    return dict_to_json_response({}, HTTPStatus.NOT_IMPLEMENTED)
    # if len(request.data) == 0:
    #    return dict_to_json_response({"error": "No payload"}, HTTPStatus.OK)
    # doc = request.get_json()
    # app.logger.debug(doc)

    # context = doc['context']
    # if 'city' not in context:
    #    return dict_to_json_response({"error": "City not provided"}, HTTPStatus.OK)
    # city = context['city']
    units = 'imperial'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_API_KEY}&units={units}'

    headers = {
        'accept': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    response.raise_for_status()

    doc = response.json()

    app.logger.debug(doc)
    coord = doc['coord']
    weather = doc['weather']
    main = doc['main']
    wind = doc['wind']
    sys = doc['sys']
    sunrise = datetime.fromtimestamp(int(sys['sunrise']))
    sunset = datetime.fromtimestamp(int(sys['sunset']))
    data = {
        "longitude": str(coord['lon']),
        "latitude": str(coord['lat']),
        "main": str(weather[0]['main']),
        "description": str(weather[0]['description']),
        "icon": str(weather[0]['icon']),
        "temperature": str(main['temp']),
        "feels_like": str(main['feels_like']),
        "temperature_min": str(main['temp_min']),
        "temperature_max": str(main['temp_max']),
        "pressure": str(main['pressure']),
        "humidity": str(main['humidity']),
        "wind_speed": str(wind['speed']),
        "wind_deg": str(wind['deg']),
        "country": str(sys['country']),
        "sunrise": str(sunrise.strftime('%Y-%m-%d %H:%M:%S')),
        "sunset": str(sunset.strftime('%Y-%m-%d %H:%M:%S'))
    }
    return dict_to_json_response(data, HTTPStatus.OK)

