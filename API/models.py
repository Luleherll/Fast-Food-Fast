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
        res = jsonify(msg='Signup successful. You can login now.'), 201
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
                return jsonify(msg="User named {} already exists.".format(
                                        clean['username'])), 406

        return res

    def login(self, username, password):
        response = self.db.run(("""SELECT user_id FROM Users WHERE
                                username = %s and password = %s""",),
                               (username, password,), 'SELECT')
        user_id = Check().unwrap(response)
        print(user_id)
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

        return jsonify(orders), 200

    def user_history(self, user_id):
        orders = self.db.run(("""SELECT * FROM orders WHERE
                                user_id = %s and status = %s""",),
                             (user_id, 'Completed'), 'SELECT')

        return orders

    def make_admin(self, user_id, username):
        if Check().is_admin(user_id) is True:
            updated = self.db.run(("""UPDATE users SET role = %s
                                WHERE username = %s""",),
                                  ('Admin', username,), 'UPDATE')
            if updated == 0:
                return jsonify(msg='User not found.'), 404
            else:
                return jsonify(msg='{} made administrator.'), 205
        else:
            return jsonify(msg='Not Authorized'), 401


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
            return jsonify(msg='Food option added successfully.'), 201
        else:
            return jsonify(msg='Not Authorized'), 401

    def get_food(self, details, name):
        if details == 'no':
            food = self.db.run(("""SELECT food_id FROM menu WHERE
                                name = %s""",), (name,), 'SELECT')
        elif details == 'yes':
            food = self.db.run(("""SELECT * FROM menu WHERE
                                name = %s""",), (name,), 'SELECT')
        return jsonify(food), 200

    def update_food(self, user_id, name, key, value):
        res = jsonify(msg='Not Authorized'), 401
        if Check().is_admin(user_id) is True:
            updated = self.db.run(("""UPDATE menu SET {} = %s
                                WHERE name = %s""".format(key),),
                                  (value, name,), 'UPDATE')
            if updated != 0:
                res = jsonify(updated), 205
            else:
                res = jsonify(msg='Not updated. crosscheck the given values.'),
                404
        else:
            return res

    def delete_food(self, user_id, food_id):
        if Check().is_admin(user_id) is True:
            self.db.run(("""DELETE FROM menu WHERE
                        food_id = %s""",), (food_id,))
            return jsonify(msg='Food successfully deleted.'), 100
        else:
            return jsonify(msg='Not Authorized'), 401

    def get_menu(self):
        menu = self.db.run(("""SELECT * FROM menu""",), command='SELECT')
        return jsonify(menu), 200


class Orders:

    def __init__(self):
        from API.routes import app
        self.db = Database(app)

    def make_order(self, user_id, order):
        user = Check().user_exists(user_id)
        food = Check().food_exists(order['name'])

        if food is None:
            return jsonify(msg='Food name you specified is not found.'), 404
        else:
            sql = ("""
             INSERT INTO orders(user_id, food_id, name, quantity, comment,
             location, amount, status)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING order_id;
            """,)
            self.db.run(sql, (user['user_id'], food['food_id'], order['name'],
                              order['quantity'], order['comment'],
                              user['location'], order['quantity']*food['price'],
                              'Queued'), 'INSERT')
        return jsonify(msg='Your order was placed successfully.'), 201

    def get_order(self, user_id, order_id):
        if Check().is_admin(user_id) is True:
            order = self.db.run(("""SELECT * FROM orders WHERE
                                 order_id = %s""",), (order_id,), 'SELECT')
            getter = Check().unwrap(order)
            if getter is None:
                return jsonify(msg='Order not found.'), 404
            else:
                return jsonify(getter), 200
        else:
            return jsonify(msg='Not Authorized'), 401

    def update_order(self, user_id, order_id, status):
        if Check().is_admin(user_id) is True:
            updated = self.db.run(("""UPDATE orders SET status = %s
                                WHERE order_id = %s""",),
                                  (status, order_id,), 'UPDATE')
            if updated != 0:
                return jsonify(msg='Successfully updated.'), 205
            else:
                return jsonify(msg='Order not found.'), 404
        else:
            return jsonify(msg='Not Authorized'), 401

    def delete_order(self, user_id, order_id):
        res = jsonify(msg='Not Authorized'), 401
        if Check().is_admin(user_id) is True:
            info = self.db.run(("""DELETE FROM orders WHERE
                        order_id = %s""",), (order_id,))
            if info is not None:
                res = jsonify(msg='Order successfully deleted.'), 100
            else:
                res = jsonify(msg='Not deleted. does it exist ?'), 404
        else:
            return res

    def get_orders(self, user_id):
        if Check().is_admin(user_id) is True:
            orders = self.db.run(("""SELECT * FROM orders""",),
                                 command='SELECT')

            return jsonify(orders), 200
        else:
            return jsonify(msg='Not Authorized'), 401
