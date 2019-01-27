from API.db import Database
from API.validation import Check
from flask import jsonify
from datetime import datetime


class Users:

    def __init__(self):
        from API.routes import app
        self.db = Database(app)

    def register(self, user):
        sql = ("""
        INSERT INTO users(username, password, tel, email, location, key_point,
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
            print(info)
            if info is not None:
                return jsonify(msg="User named {} already exists.".format(
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

        return jsonify(orders), 200

    def user_history(self, user_id):
        orders = self.db.run(("""SELECT * FROM orders WHERE
                                user_id = %s and status = 'Completed' UNION
                                SELECT * FROM orders WHERE user_id = %s and
                                status = 'Declined'""",),
                             (user_id, user_id,), 'SELECT')

        return orders

    def make_admin(self, user_id, username):
        if Check().is_admin(user_id) is True:
            updated = self.db.run(("""UPDATE users SET role = %s
                                WHERE username = %s""",),
                                  ('Admin', username,), 'UPDATE')
            print(updated)
            if updated == 0:
                return jsonify(msg='User not found.'), 404
            else:
                return jsonify(msg='{} made administrator.'.format(username)), 200
        else:
            return jsonify(msg='Not Authorized'), 401


class Menu:

    def __init__(self):
        from API.routes import app
        self.db = Database(app)

    def add_food(self, user_id, food):
        sql = ("""
        INSERT INTO menu(name, price, status, tags, img1, img2, img3)
             VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING food_id;
        """,)
        if Check().is_admin(user_id) is True:
            info = self.db.run(sql, (food['name'], food['price'],
                               food['status'], food['tags'], food['img1'],
                               food['img2'], food['img3']), 'INSERT')
            if info is not None:
                return jsonify(msg='Food already exists.Try updating.'), 406
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

    def update_food(self, user_id, update):
        res = jsonify(msg='Not Authorized'), 401
        if Check().is_admin(user_id) is True:
            updated = self.db.run(("""UPDATE menu SET price = %s, status = %s,
                                    tags = %s, img1 = %s, img2 = %s, img3 = %s WHERE name = %s""",),
                                  (update['price'], update['status'],
                                  update['tags'], update['img1'],
                               update['img2'], update['img3'], update['name']), 'UPDATE')
            print(updated)
            if updated != 0:
                return jsonify(msg='Food updated successfully.'), 200
            else:
                return jsonify(msg='Not updated. crosscheck the given values.'), 404
        else:
            return res

    def delete_food(self, user_id, name):
        if Check().is_admin(user_id) is True:
            self.db.run(("""DELETE FROM menu WHERE
                        name = %s""",), (name,))
            return jsonify(msg='Food successfully deleted.'), 200
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
             location, amount, status, created_at, img1)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING order_id;
            """,)
            info = self.db.run(sql, (user['user_id'], food['food_id'], order['name'],
                              order['quantity'], order['comment'],
                              user['location'], order['quantity']*food['price'],
                              'Queued', datetime.now().strftime("%A, %d. %B %Y %I:%M%p"),
                               food['img1']), 'INSERT')
            if info is not None:
                return jsonify(msg=str(info)), 201
        
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
            updated = self.db.run(("""UPDATE orders SET status = %s, ended_at = %s
                                WHERE order_id = %s""",),
                                  (status, datetime.now().strftime("%A, %d. %B %Y %I:%M%p"),
                                   order_id,), 'UPDATE')
            if updated != 0:
                return jsonify(msg='Successfully updated.'), 200
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
                res = jsonify(msg='Order successfully deleted.'), 200
            else:
                res = jsonify(msg='Not deleted. does it exist ?'), 404
        else:
            return res

    def get_new_orders(self, user_id):
        if Check().is_admin(user_id) is True:
            orders = self.db.run(("""SELECT * FROM orders WHERE
                                  status = 'Queued'""",),
                                 command='SELECT')
            print(orders)
            return jsonify(orders), 200
        else:
            return jsonify(msg='Not Authorized'), 401

    def get_pending_orders(self, user_id):
        if Check().is_admin(user_id) is True:
            orders = self.db.run(("""SELECT * FROM orders WHERE status =
                                     'Pending'""",),
                                 command='SELECT')

            return jsonify(orders), 200
        else:
            return jsonify(msg='Not Authorized'), 401

    def complete_and_decline(self, user_id):
        if Check().is_admin(user_id) is True:
            orders = self.db.run(("""SELECT * FROM orders WHERE status = 'Completed'
                               UNION all SELECT * FROM orders WHERE status = 'Declined'""",),
                                 command='SELECT')
            print(orders)
            return jsonify(orders), 200
        else:
            return jsonify(msg='Not Authorized'), 401
