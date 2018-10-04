from API.models import Users, Orders, Menu
from API.validation import Check
from flask import Flask, jsonify
from flask import request, session
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'ucanguessit'
jwt = JWTManager(app)


@app.route('/')
def welcome():
    return jsonify("Welcome to the Fast-Food-Fast API")


@app.errorhandler(404)
def not_found_error(e):
    return "<h1>You're lost in the woods:<br> Go back to index:<h1>\
<a href='https://lule-fast-food.herokuapp.com/'>Click Here<a>", 404


@app.route('/api/v2/auth/signup', methods=['POST'])
def register():
    "This route registers a new user."
    try:
        name = request.get_json()['username']
        password = request.get_json()['password']
        tel = request.get_json()['tel']
        email = request.get_json()['email']
        location = request.get_json()['location']
        key_point = request.get_json()['key point']

        user = {'username': name, 'password': password, 'tel': tel,
                'email': email, 'location': location,
                'key_point': key_point}
        response = Users().register(user)

        return response
    except KeyError:
        return jsonify('Missing data'), 400
    except ValueError:
        return jsonify('Invalid data'), 400
    

@app.route('/api/v2/auth/login', methods=['POST'])
def login():
    "This route logs in a user."
    try:
        name = request.get_json()['username']
        password = request.get_json()['password']
        clean = Check().is_clean({'username': name, 'password': password})
        if type(clean) == tuple:
            return clean
        else:
            user_id = Users().login(name, password)
            access_token = create_access_token(identity=user_id[0])
            return jsonify(access_token), 200
    except TypeError:
        return jsonify('Not Registered.'), 401
    except KeyError:
        return jsonify('Missing data'), 400


@app.route('/api/v2/users/orders', methods=['GET', 'POST'])
@jwt_required
def place_order():
    user_id = get_jwt_identity()
    "This route adds a new order to the orders list."
    if request.method == 'POST':
        try:
            name = request.get_json()['name']
            quantity = request.get_json()['quantity']
            comment = request.get_json()['comment']
            order = {'name': name, 'quantity': quantity, 'comment': comment}

            response = Orders().make_order(user_id, order)
            return response
        except KeyError:
            return jsonify('Missing data'), 400
        except ValueError:
            return jsonify('Invalid data'), 400

    elif request.method == 'GET':
        "This route returns the history of orders."
        response = Users().user_history(user_id)
        return jsonify(response)


@app.route('/api/v2/orders/<int:orderId>', methods=['GET', 'PUT'])
@jwt_required
def get_order(orderId):
    user_id = get_jwt_identity()
    "This route returns the details of a particular order."
    if request.method == 'GET':
        order = Orders().get_order(user_id, orderId)
        return order

    elif request.method == 'PUT':
        "This route updates the status key of a particular order."
        status = request.get_json()['status']
        response = Orders().update_order(user_id, orderId, status)
        return response


@app.route('/api/v2/orders/', methods=['GET'])
@jwt_required
def get_orders():
    "This route returns all orders."
    user_id = get_jwt_identity()
    response = Orders().get_orders(user_id)
    return response


@app.route('/api/v2/menu', methods=['GET', 'POST'])
@jwt_required
def menu():
    "This route returns all the food items in the food list."
    user_id = get_jwt_identity()
    if request.method == 'GET':
        response = Menu().get_menu()
        return response

    elif request.method == 'POST':
        name = request.get_json()['name']
        price = request.get_json()['price']
        status = request.get_json()['status']
        tags = request.get_json()['tags']
        food = {'name': name, 'price': price, 'status': status,
                'tags': tags}
        response = Menu().add_food(user_id, food)
        return response
