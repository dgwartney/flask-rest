#!/usr/bin/env python
import os
import json
from http import HTTPStatus
from flask import Flask
from flask import render_template
from flask import request
from flask import Response

from rest.databases.shoes import get_products, get_product_by_id

# Set our default listening port to 3000
port = 3000
# If the PORT environment variable is set
# then use the value from the variable
if 'PORT' in os.environ:
    port = os.environ['PORT']

host = 'localhost'
# Default binding to the localhost set
# the HOST environment variable to override
if 'HOST' in os.environ:
    host = os.environ['HOST']

# create the application object
app = Flask(__name__)


# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('welcome.html')  # render a template


@app.route('/products', methods=['GET'])
def search_for_orders():
    app.logger.debug(f"Content-Type: {request.content_type}")
    app.logger.debug(f"Args: {type(request.args)}")
    response = Response(response=json.dumps(get_products()).encode('utf-8'),
                        status=HTTPStatus.OK,
                        content_type='application/json')
    return response


@app.route('/products/item/<product_id>', methods=['GET'])
def get_order(product_id):
    response = None
    app.logger.debug(request.headers)
    if request.headers['accept'] != 'application/json':
        response = Response(response=json.dumps({"result": "Incorrect accept header"}).encode('utf-8'),
                            status=HTTPStatus.METHOD_NOT_ALLOWED,
                            content_type='application/json')

    elif product_id is None:
        response = Response(response=json.dumps({"result": "Product Id Missing"}).encode('utf-8'),
                            status=HTTPStatus.BAD_REQUEST,
                            content_type='application/json')
    elif get_product_by_id(product_id) is not None:
        product = get_product_by_id(product_id)
        response = Response(response=json.dumps(product),
                            status=HTTPStatus.OK,
                            content_type='application/json')
    else:
        response = Response(response=json.dumps({"result": "Product Not Found"}).encode('utf-8'),
                            status=HTTPStatus.NOT_FOUND,
                            content_type='application/json')
    return response


@app.route('/products', methods=['POST'])
def lookup_order(order_id):
    response = None
    app.logger.debug(f"Content-Type: {request.content_type}")
    app.logger.debug(f"Type: {type(request.data)}")
    app.logger.debug(request.data)
    if request.data is None:
        response = Response(response={"request": "Product id not specified"},
                            status=HTTPStatus.BAD_REQUEST,
                            content_type='application/json')
    elif request.content_type != 'application/json':
        response = Response(response={"result": "Incorrect accept header"},
                            status=HTTPStatus.METHOD_NOT_ALLOWED,
                            content_type='application/json')
    else:
        doc = json.loads(request.data)
        product_id = doc['product_id']
        if 'product_id' in doc:
            product = get_product_by_id(product_id)

            response = Response(response=json.dumps(product).encode('utf-8'),
                                status=HTTPStatus.OK,
                                content_type='application/json')
        else:
            response = Response(response={"request": "Product id not specified"},
                                status=HTTPStatus.BAD_REQUEST,
                                content_type='application/json')
    return response


# start the server with the 'run()' method
if __name__ == '__main__':
    try:
        app.run(host=host, port=port, debug=True)
    except Exception as e:
        app.logger.exception(e)
