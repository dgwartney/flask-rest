#!/usr/bin/env python
import json
from http import HTTPStatus

from flask import Flask
from flask import Response
from flask import render_template
from flask import request

from rest.databases.shoes import get_products, get_product_by_id

# create the application object
app = Flask(__name__)


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
# Returns all of the products in the catalog
#
@app.route('/products', methods=['GET'])
def search_for_orders():
    # if 'accept' not in request.headers or request.headers['accept'] != 'application/json':
    #     response = dict_to_json_response({"result": "Incorrect accept header"}, HTTPStatus.METHOD_NOT_ALLOWED)
    # else:
    response = dict_to_json_response({"products": get_products()}, status=HTTPStatus.OK)
    return response


#
# Returns a product from the catalog by its product id using HTTP GET
#
@app.route('/products/item/<product_id>', methods=['GET'])
def get_order(product_id):
    response = None
    app.logger.debug(request.headers)
    # if 'accept' not in request.headers or request.headers['accept'] != 'application/json':
    #     response = dict_to_json_response({"result": "Incorrect accept header"}, HTTPStatus.METHOD_NOT_ALLOWED)
    if product_id is None:
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
    #    elif 'accept' not in request.headers or request.headers['accept'] != 'application/json':
    #        response = dict_to_json_response({"result": "Incorrect accept header"}, HTTPStatus.METHOD_NOT_ALLOWED)
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


#
# Looks up the status of an order
#
@app.route('/orders/<order_id>', methods=['GET'])
def find_order(order_id):
    """
    Looks up the status of an order
    """
    app.logger.info(f"Searching for order with order id: {order_id}")
    return {"order_status": "entregado"}


#
# Call by an action task
#
@app.route('/notifications/<notification_id>', methods=['GET'])
def notifications(notification_id):
    return {"message": "Hello World!"}
