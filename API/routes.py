from API.models import Users, Orders, Menu
from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

"""if __name__ == '__main__':
    u = {'username': 'lule', 'password': 'dev', 'tel': '07777',
         'email': 'lule@dev.com', 'location': 'Nalya',
         'key point': 'Acacia mall entrance'}
    x = Users().register(u)
    print(x)
    m = Users().login('lule', 'admin')
    print(m)
partial_content = 'You must provide the required values.'
invalid = 'The server encountered an error which is due\
 to an invalid data type. Valid format: '"""


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


@app.route('/api/v2/auth/login', methods=['POST'])
def login():
    "This route registers a new user."
    name = request.get_json()['username']
    password = request.get_json()['password']
    response = Users().login(name, password)
    return response

"""@app.route('/api/v2/users/orders', methods=['GET', 'POST'])
def place_order():
    "This route adds a new order to the orders list."
    if request.method == 'POST':
        name = request.get_json()['name']
        quantity = request.get_json()['quantity']
        comment = request.get_json()['comment']
        order = Order(name, quantity, comment)

        response = Orders().make_order(order)
        return response

    elif request.method == 'GET':
        "This route returns the list of orders."
        response = Orders().user_history(user_id)
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
            state = request.get_json()['status'].strip(' ')
            check = missing([state])
            if check is not True:
                return check
            else:
                pass
        except KeyError:
            return jsonify(partial_content + ' [status]'), 400
        except AttributeError:
            return jsonify(invalid + '[letters]'), 400

        response = orders.update_order(order, state)
        return response"""


"""@app.route('/api/v2/menu', methods=['GET'])
def menu():
    "This route returns all the food items in the food list."
    response = Menu().get_menu()
    #return response
    print(response)


@app.route('/api/v1/menu/add', methods=['POST'])
def add_food_item():
    "This route adds a food item to the food list."
    try:
        name = request.get_json()['name'].strip(' ')
        price = int(request.get_json()['price'])
        ready_in = request.get_json()['ready in'].strip(' ')
        status = request.get_json()['status'].strip(' ')
        units = request.get_json()['units'].strip(' ')
        tags = request.get_json()['tags'].strip(' ')
        check = missing([name, price, ready_in, status, units, tags])
        if check is not True:
            return check
        else:
            pass
    except KeyError:
        return jsonify(partial_content + ' [name, price, ready in,\
 status, units, tags'), 400
    except ValueError:
        return jsonify(invalid + '[letters,numbers,letters for all the rest]\
'), 400
    except AttributeError:
        return jsonify(invalid + '[letters,numbers,letters for all the rest]\
'), 400

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
        return response"""
