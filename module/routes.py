from module.api import Order, Orders, jsonify
from flask import Flask
from flask import request

app = Flask(__name__)
orders = Orders()


@app.route('/')
def welcome():
    return "<h1>Welcome to the Fast-Food-Fast API<h1>"


@app.route('/api/v1/orders', methods=['POST'])
def place_order():
    "This route adds a new order to the orders list when parsed with a json\
 object containing all required values."
    try:
        name = request.get_json()['name']
        quantity = request.get_json()['quantity']
        time = request.get_json()['time']
        customer = request.get_json()['user_id']
        where = request.get_json()['location']
    except KeyError:
        return jsonify('You must provide all required values. [name, quantity,\
time, user_id, location]'), 206

    order = Order(name, quantity, time, customer, where)
    response = orders.place_order(order)

    return response


@app.route('/api/v1/orders', methods=['GET'])
def all_orders():
    "This route returns the list of orders."
    response = orders.all_orders()
    return response


@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    "This route returns the details of a particular order."
    order = order_id
    response = orders.get_order(order)

    return response


@app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    "This route updates the status key of a particular order."
    order = order_id
    try:
        state = request.get_json()['status']
    except KeyError:
        return jsonify('You must provide the required value. [status]'), 206

    response = orders.update_order(order, state)

    return response
