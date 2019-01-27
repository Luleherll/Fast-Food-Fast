from API.models import Users, Orders, Menu
from API.validation import Check
from flask import Flask, jsonify
from flask import request, redirect
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from flasgger import Swagger, swag_from
from flask_cors import CORS
import datetime


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'ucanguessit'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=2)
jwt = JWTManager(app)
Swagger(app)
CORS(app)
error = 'You must provide all required fields.'


@app.route("/")
def index():
    return redirect('/apidocs')


@app.errorhandler(404)
def not_found_error(e):
    return "<h1>You're lost in the woods:<br> Go back to index:<h1>\
<a href='https://lule-persistent.herokuapp.com/'>Click Here<a>", 404


@app.route('/api/v2/auth/signup', methods=['POST'])
@swag_from('docs/signup.yml')
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
        return jsonify(error=error), 400
    except ValueError:
        return jsonify(error='Please provide valid data types.'), 400


@app.route('/api/v2/auth/login', methods=['POST'])
@swag_from('docs/login.yml')
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
            access_token = create_access_token(identity=user_id['user_id'])
            userStatus = Check().is_admin(user_id)
            
            return jsonify({'token': access_token, 'status': userStatus}), 200
    except TypeError:
        return jsonify(error='Not Registered.'), 401
    except KeyError:
        return jsonify(error=error), 400


@app.route('/api/v2/auth/admin', methods=['PUT'])
@jwt_required
@swag_from('docs/make_admin.yml')
def make_admin():
    user_id = get_jwt_identity()
    "This route makes user admins."
    try:
        name = request.get_json()['username']
        clean = Check().is_clean({'username': name})
        if type(clean) == tuple:
            return clean
        else:
            response = Users().make_admin(user_id, name)
            return response
    except TypeError:
        return jsonify(error='Not Registered.'), 401
    except KeyError:
        return jsonify(error=error), 400


@app.route('/api/v2/users/orders', methods=['POST'])
@jwt_required
@swag_from('docs/make_order.yml')
def place_order():
    user_id = get_jwt_identity()
    "This route adds a new order to the orders list."
    try:
        name = request.get_json()['name']
        quantity = request.get_json()['quantity']
        comment = request.get_json()['comment']
        order = {'name': name, 'quantity': quantity, 'comment': comment}
        clean = Check().is_clean(order)
        if type(clean) == tuple:
            return clean
        else:
            response = Orders().make_order(user_id, order)
            return response

    except KeyError:
        return jsonify(error=error), 400


@app.route('/api/v2/users/orders', methods=['GET'])
@jwt_required
@swag_from('docs/user_orders.yml')
def user_orders():
    user_id = get_jwt_identity() 
    "This route returns the history of orders."
    response = Users().user_orders(user_id)
    return response


@app.route('/api/v2/users/history', methods=['GET'])
@jwt_required
@swag_from('docs/user_history.yml')
def user_history():
    user_id = get_jwt_identity()
    "This route returns the history of orders."
    response = Users().user_history(user_id)
    return jsonify(response)


@app.route('/api/v2/orders/<int:orderId>', methods=['GET'])
@jwt_required
@swag_from('docs/get_order.yml')
def get_order(orderId):
    user_id = get_jwt_identity()
    "This route returns the details of a particular order."
    order = Orders().get_order(user_id, orderId)
    return order


@app.route('/api/v2/orders/<int:orderId>', methods=['PUT'])
@jwt_required
@swag_from('docs/update_order.yml')
def update_order(orderId):
    user_id = get_jwt_identity()
    "This route updates the status key of a particular order."
    status = request.get_json()['status']
    response = Orders().update_order(user_id, orderId, status)
    return response
  
  
@app.route('/api/v2/orders/<int:orderId>', methods=['DELETE'])
@jwt_required
def delete_order(orderId):
    user_id = get_jwt_identity()
    "This route deletes a particular order."
    response = Orders().delete_order(user_id, orderId)
    return response


@app.route('/api/v2/orders/', methods=['GET'])
@jwt_required
@swag_from('docs/orders.yml')
def get_orders():
    "This route returns all orders."
    user_id = get_jwt_identity()
    response = Orders().get_new_orders(user_id)
    return response

@app.route('/api/v2/orders/pending', methods=['GET'])
@jwt_required
def pending_orders():
    "This route returns all orders."
    user_id = get_jwt_identity()
    response = Orders().get_pending_orders(user_id)
    return response


@app.route('/api/v2/orders/archive', methods=['GET'])
@jwt_required
def archive():
    "This route returns all orders."
    user_id = get_jwt_identity()
    response = Orders().complete_and_decline(user_id)
    return response


@app.route('/api/v2/menu', methods=['GET'])
@jwt_required
@swag_from('docs/menu.yml')
def menu():
    "This route returns all the food items in the food list."
    response = Menu().get_menu()
    return response


@app.route('/api/v2/menu', methods=['POST'])
@jwt_required
@swag_from('docs/add_food.yml')
def add_menu():
    user_id = get_jwt_identity()
    try:
        img1 = request.get_json()['img1']
        img2 = request.get_json()['img2']
        img3 = request.get_json()['img3']
        name = request.get_json()['name']
        price = request.get_json()['price']
        status = request.get_json()['status']
        tags = request.get_json()['tags']
        food = {'name': name, 'price': price, 'status': status,
                'tags': tags, 'img1': img1, 'img2': img2, 'img3': img3}
        clean = Check().is_clean(food)
        if type(clean) == tuple:
            return clean
        else:
            response = Menu().add_food(user_id, food)
            return response
    except KeyError:
        return jsonify(error=error), 400


@app.route('/api/v2/menu', methods=['PUT'])
@jwt_required
def update_food():
    user_id = get_jwt_identity()
    try:
        img1 = request.get_json()['img1']
        img2 = request.get_json()['img2']
        img3 = request.get_json()['img3']
        name = request.get_json()['name']
        price = request.get_json()['price']
        status = request.get_json()['status']
        tags = request.get_json()['tags']
        food = {'name': name, 'price': price, 'status': status,
                'tags': tags, 'img1': img1, 'img2': img2, 'img3': img3}
        clean = Check().is_clean(food)
        if type(clean) == tuple:
            return clean
        else:
            response = Menu().update_food(user_id, food)
            return response
    except KeyError:
        return jsonify(error=error), 400

@app.route('/api/v2/menu', methods=['DELETE'])
@jwt_required
def delete_food():
    user_id = get_jwt_identity()
    try:
        name = request.get_json()['name']
        response = Menu().delete_food(user_id, name)
        return response
    except KeyError:
        return jsonify(error=error), 400
