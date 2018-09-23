from module.api import Order, Orders, FoodList, Users
from flask import Flask, jsonify
from flask import request

app = Flask(__name__)
orders = Orders()
foods = FoodList()
users = orders.users
partial_content = 'You must provide the required values.'


@app.route('/')
def welcome():
    return "<h1>Welcome to the Fast-Food-Fast API<h1>"


@app.route('/api/v1/register', methods=['POST'])
def register():
    "This route registers a new user."
    try:
        name = request.get_json()['username']
        email = request.get_json()['email']
        location = request.get_json()['location']
        key_point = request.get_json()['key point']
    except KeyError:
        return jsonify(partial_content + '[username, email, location,\
 key point]'), 400

    user = {'username': name, 'email': email, 'location': location,
            'key point': key_point}
    response = users.register(user)
    return response


@app.route('/api/v1/orders', methods=['GET', 'POST'])
def place_order():
    "This route adds a new order to the orders list when parsed with a json\
 object containing all required values."
    if request.method == 'POST':
        try:
            name = request.get_json()['name']
            quantity = request.get_json()['quantity']
            comment = request.get_json()['comment']
            customer = request.get_json()['username']
        except KeyError:
            return jsonify(partial_content + ' [name, quantity, comment,\
 username]'), 400

        order = Order(name, quantity, comment, customer)
        response = orders.place_order(order)
        return response

    elif request.method == 'GET':
        "This route returns the list of orders."
        response = orders.all_orders()
        return response


@app.route('/api/v1/orders/<int:order_id>', methods=['GET', 'PUT'])
def get_order(order_id):
    "This route returns the details of a particular order."
    if request.method == 'GET':
        order = order_id
        response = orders.get_order(order)
        return response

    elif request.method == 'PUT':
        "This route updates the status key of a particular order."
        order = order_id
        try:
            state = request.get_json()['status']
        except KeyError:
            return jsonify(partial_content + ' [status]'), 400

        response = orders.update_order(order, state)
        return response


@app.route('/api/v1/menu', methods=['GET'])
def menu():
    "This route returns all the food items in the food list."
    response = foods.get_menu()
    return response


@app.route('/api/v1/menu/add', methods=['POST'])
def add_food_item():
    "This route adds a food item to the food list."
    try:
        name = request.get_json()['name']
        price = request.get_json()['price']
        ready_in = request.get_json()['ready in']
        status = request.get_json()['status']
        units = request.get_json()['units']
        tags = request.get_json()['tags']
    except KeyError:
        return jsonify(partial_content + ' [name, price, ready in,\
 status, units, tags'), 400

    food_item = {'name': name, "price": price, 'ready in\
': ready_in, 'status': status, 'units': units, 'tags\
': tags}

    response = foods.add_food_item(food_item)
    return response


@app.route('/api/v1/menu/<string:name>', methods=['PUT', 'DELETE'])
def update_food_item(name):
    if request.method == 'PUT':
        "This route updates the details of a particular food item."
        food_name = name
        updates = request.get_json()
        response = foods.update_food_item(food_name, updates)
        return response

    elif request.method == 'DELETE':
        "This route deletes a particular food item from the food list."
        food_name = name
        response = foods.delete_food_item(food_name)
        return response
