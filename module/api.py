from flask import Flask
from flask import jsonify


class Users:

    def __init__(self):
        self.users = [{'username': 'lule', 'email': 'lule@dev.com\
', 'location': 'Kasubi', 'key point': 'Tombs'}]

    def check(self, person):
        for user in self.users:
            if user['username'] == person['username']:
                return True
        return False

    def register(self, user):
        check = self.check(user)
        if check is True:
            return jsonify('User named {} already exists.'.format(user['\
username'])), 403
        else:
            self.users.append(user)
            return jsonify('Registration successful.'), 200

    def get_user(self, name):
        for user in self.users:
            if user['username'] == name:
                return user
        return None


class FoodList:
    "This class handles menu related issues of Fast-Food-Fast."
    def __init__(self):
        "This initializes the dictionary where all food items will be."
        self.food_list = {}

    def check(self, name):
        "This method checks if a food item exists in the food_list and returns\
 it or `None` if not found."
        for key in self.food_list:
            if key == name:
                return self.food_list[key]
        else:
            return

    def not_found(self, name):
        "This method returns a response containing a `not found`\
 message with a `404` status code"
        return jsonify('Food with name: {} not found in food list'.format
                       (name)), 404

    def success(self, name, act):
        "This method returns a response containing a `success` message with\
 a `200` status code."
        return jsonify('[{}] {} successfully.'.format(name, act)), 200

    def add_food_item(self, item):
        "This method adds a food item to the food list."
        check = self.check(item['name'])
        if check is not None:
            return jsonify('Food with name: {} already exists. Try updating.\
'.format(item['name'])), 501
        else:
            self.food_list[item['name']] = item

            return self.success(item['name'], 'added')

    def update_food_item(self, name, updates):
        "This method updates a particular food item if it exists in the food\
 list."
        food_item = self.check(name)
        if food_item is None:
            return self.not_found(name)
        else:
            for key in food_item:
                for update in updates:
                    if key == update:
                        food_item[key] = updates[update]
            return self.success(name, 'updated')

    def delete_food_item(self, name):
        "This method deletes a food item from the food list if it exists."
        try:
            self.food_list.pop(name)
            return self.success(name, 'deleted')
        except KeyError:
            return self.not_found(name)

    def get_menu(self):
        "This returns the food list with all the food items."
        return jsonify(self.food_list), 200


class Order:
    "Order class is being used to create the order object when given all the\
 required parameters."
    def __init__(self, name, quantity, comment, customer):
        self.name = name
        self.quantity = quantity
        self.comment = comment
        self.customer = customer


class Orders:
    "A class that handles the placing, updating and retrieving of orders."
    def __init__(self):
        "Initializes the orders list for storing all orders and an integer\
 for assigning an `id` to every order."
        self.orders = []
        self.users = Users()
        self.n = 1

    def check(self, order_id):
        """This method checks if a particular order exists in the orders list \
when given the order id. If it exists, returns the order and `False` if it\
 doesnot exist."""
        for order in self.orders:
            if order['id'] == order_id:
                return order

        return False

    def not_found(self, order_id):
        "This when given the order id returns a response containing a `not found`\
 message with a `404` status code"
        return jsonify('Order with Id: {} not found.'.format(order_id)), 404

    def status(self, order_id, state):
        """This method when given the order id and a letter corresponding to any\
 of the specified states, adds a `status` key and value to the order with a\
 given `id`. If order doesnot exist, a `not_found(order_id)` method is called.
        """
        states = ['Queued', 'Pending', 'Completed', 'Undefined']
        for status in states:
            if state == status[0]:
                state = status

        order = self.check(order_id)
        if order is False:
            return self.not_found(order_id)
        else:
            order['status'] = state

    def success(self, act, order_id):
        "This method returns a response containing a `successful` message\
 that shows the operation that was successful with a `200` status code."
        if act == 'P':
            act = 'placed'
        elif act == 'U':
            act = 'updated'

        return jsonify('Your order was successfully {}. Order Id: \
{}'.format(act, order_id)), 200

    def strip(self, order):
        "When given the order object, this method creates a dictionary using\
 the `order` attributes and returns it."
        user = self.users.get_user(order.customer)
        if user is not None:
            sheet = {'id': self.n, 'name': order.name, 'quan\
tity': order.quantity, 'comment': order.comment, 're\
quester': order.customer, 'where': user['location']}
        else:
            return None

        return sheet

    def place_order(self, order):
        "This method gets and adds the value of `strip(order)` to the orders list\
 and returns the value of `success(act, order_id)` method."
        sheet = self.strip(order)
        if sheet is None:
            return jsonify('User named {} is not registered.'.format(order
                           .customer)), 401
        else:
            order_id = self.n
            self.orders.append(sheet)
            self.status(self.n, 'Q')
            self.n += 1

        return self.success('P', order_id)

    def get_order(self, order_id):
        "When given the order id, this method returns a response containing\
 the order with the given `id` and a `200` status code. If order doesnot \
exist, returns the value of `not_found(order_id)` method."
        order = self.check(order_id)
        if order is False:
            return self.not_found(order_id)
        else:
            return jsonify(order), 200

    def update_order(self, order_id, state):
        "This method updates the order status by calling the `status(order_id,\
state)` method. If the update is a success, then it returns the value\
 of the `success(act, order_id)` method."
        updated = self.status(order_id, state)
        if type(updated) == tuple:
            return updated
        else:
            return self.success('U', order_id)

    def all_orders(self):
        "This returns a response containing a list of orders with a `200`\
 status code."
        return jsonify(self.orders), 200
