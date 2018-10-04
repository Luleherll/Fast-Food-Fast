from API.db import Database
from API.validation import Check
from flask import jsonify


class Users:

    def __init__(self):
        from API.routes import app
        self.db = Database(app)

    def register(self, user):
        sql = ("""
        INSERT INTO Users(username, password, tel, email, location, key_point,
                          role)
             VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;
        """,)
        res = jsonify('Signup successful. You can login now.'), 201
        clean = Check().is_clean(user)
        if type(clean) == tuple:
            res = clean

        else:
            info = self.db.run(sql, (clean['username'], clean['password'],
                                     clean['tel'], clean['email'],
                                     clean['location'],
                                    clean['key_point'], 'User'),
                                    'INSERT')
            if info is not None:
                res = jsonify("User named {} already exists.".format(
                                        clean['username'])), 406

        return res

    def login(self, username, password):
        response = self.db.run(("""SELECT user_id FROM Users WHERE
                                username = %s and password = %s""",),
                               (username, password,), 'SELECT')
        user_id = Check().unwrap(response)
        return user_id
        

    def reset_password(self, username, new_password):
        updated = self.db.run(("""UPDATE users SET password = %s
                                WHERE username = %s""",),
                              (new_password, username,), 'UPDATE')
        return updated

    def user_orders(self, user_id):
        orders = self.db.run(("""SELECT * FROM orders WHERE
                                user_id = %s and status = %s""",),
                             (user_id, 'Pending'), 'SELECT')
        return orders

    def user_history(self, user_id):
        orders = self.db.run(("""SELECT * FROM orders WHERE
                                user_id = %s and status = %s""",),
                             (user_id, 'Completed'), 'SELECT')
        return orders

    def make_admin(self, username):
        updated = self.db.run(("""UPDATE users SET role = %s
                                WHERE username = %s""",),
                              ('Admin', username,), 'UPDATE')
        return updated


class Menu:

    def __init__(self):
        from API.routes import app
        self.db = Database(app)

    def add_food(self, user_id, food):
        sql = ("""
        INSERT INTO menu(name, price, status, tags)
             VALUES(%s,%s,%s,%s) RETURNING food_id;
        """,)
        if Check().is_admin(user_id) is True:
            self.db.run(sql, (food['name'], food['price'],
                        food['status'], food['tags']), 'INSERT')
            return jsonify('Food option added successfully.'), 201
        else:
            return jsonify('Not Authorized'), 401

    def get_food(self, details, name):
        if details == 'no':
            food = self.db.run(("""SELECT food_id FROM menu WHERE
                                name = %s""",), (name,), 'SELECT')
        elif details == 'yes':
            food = self.db.run(("""SELECT * FROM menu WHERE
                                name = %s""",), (name,), 'SELECT')
        return jsonify(food), 200

    def update_food(self, user_id, name, key, value):
        res = jsonify('Not Authorized'), 401
        if Check().is_admin(user_id) is True:
            updated = self.db.run(("""UPDATE menu SET {} = %s
                                WHERE name = %s""".format(key),),
                                  (value, name,), 'UPDATE')
            if updated != 0:
                res = jsonify(updated), 205
            else:
                res = jsonify('Not updated. crosscheck the given values.'), 404
        else:
            return res

    def delete_food(self, user_id, food_id):
        if Check().is_admin(user_id) is True:
            self.db.run(("""DELETE FROM menu WHERE
                        food_id = %s""",), (food_id,))
            return jsonify('Food successfully deleted.'), 100
        else:
            return jsonify('Not Authorized'), 401

    def get_menu(self):
        menu = self.db.run(("""SELECT * FROM menu""",), command='SELECT')
        store = {}
        for food in menu:
            store = {'id': food[0], 'name': food[1], 'price': food[2],
                   'status': food[3], 'tags': food[4]}
        return jsonify(store), 200


class Orders:

    def __init__(self):
        from API.routes import app
        self.db = Database(app)

    def make_order(self, order):
        sql = ("""
        INSERT INTO orders(user_id, food_id, name, quantity, comment,
        location, amount, status)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING order_id;
        """,)
        self.db.run(sql, (order['user_id'], order['food_id'], order['name'],
                          order['quantity'], order['comment'],
                          order['location'], order['amount'], 'Queued'),
                    'INSERT')
        return jsonify('Your order was placed successfully.'), 201

    def get_order(self, user_id, order_id):
        if Check().is_admin(user_id) is True:
            order = self.db.run(("""SELECT * FROM orders WHERE
                                 order_id = %s""",), (order_id,), 'SELECT')
            getter = Check().unwrap(order)
            store = {'id': getter[0], 'user_id': getter[1], 'food_id': getter[2],
                     'name': getter[3], 'quantity': getter[4],
                     'comment': getter[5], 'location': getter[6]}
            return jsonify(store), 200
        else:
            return jsonify('Not Authorized'), 401

    def update_order(self, user_id, order_id, status):
        if Check().is_admin(user_id) is True:
            updated = self.db.run(("""UPDATE orders SET status = %s
                                WHERE order_id = %s""",),
                                  (status, order_id,), 'UPDATE')
            if updated != 0:
                return jsonify('Successfully updated.'), 205
        else:
            return jsonify('Not Authorized'), 401

    def delete_order(self, user_id, order_id):
        res = jsonify('Not Authorized'), 401
        if Check().is_admin(user_id) is True:
            info = self.db.run(("""DELETE FROM orders WHERE
                        order_id = %s""",), (order_id,))
            if info is not None:
                res = jsonify('Order successfully deleted.'), 100
            else:
                res = jsonify('Not deleted. does it exist ?'), 404
        else:
            return res

    def get_orders(self, user_id):
        if Check().is_admin(user_id) is True:
            orders = self.db.run(("""SELECT * FROM orders""",),
                                 command='SELECT')
            all_orders = {}
            for order in orders:
                line = {'id': order[0], 'user_id': order[1], 'food_id': order[2],
                        'name': order[3], 'quantity': order[4],
                        'comment': order[5], 'location': order[6]}
                all_orders[order[3]] = line

            return jsonify(all_orders), 200
        else:
            return jsonify('Not Authorized'), 401
