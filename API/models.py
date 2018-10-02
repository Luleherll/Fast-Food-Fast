from API.db import Database


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
        self.db.run(sql, (user['username'], user['password'],
                    user['tel'], user['email'], user['location'],
                    user['key_point'], 'User'), 'INSERT')
        return 'Signup successful. You can login now.'

    def login(self, username, password):
        user_id = self.db.run(("""SELECT user_id FROM Users WHERE
                                username = %s and password = %s""",),
                              (username, password,), 'SELECT')
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

    def add_food(self, food):
        sql = ("""
        INSERT INTO menu(name, price, status, tags)
             VALUES(%s,%s,%s,%s) RETURNING food_id;
        """,)
        self.db.run(sql, (food['name'], food['price'],
                    food['status'], food['tags']), 'INSERT')
        return 'Food option added successfully.'

    def get_food(self, details, name):
        if details == 'no':
            food = self.db.run(("""SELECT food_id FROM menu WHERE
                                name = %s""",), (name,), 'SELECT')
        elif details == 'yes':
            food = self.db.run(("""SELECT * FROM menu WHERE
                                name = %s""",), (name,), 'SELECT')
        return food

    def update_food(self, name, key, value):
        updated = self.db.run(("""UPDATE menu SET {} = %s
                                WHERE name = %s""".format(key),),
                              (value, name,), 'UPDATE')
        return updated

    def delete_food(self, food_id):
        self.db.run(("""DELETE FROM menu WHERE
                      food_id = %s""",), (food_id,))
        return 'Food successfully deleted.'

    def get_menu(self):
        menu = self.db.run(("""SELECT * FROM menu"""), command='SELECT')
        return menu


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
        return 'Your order was placed successfully.'

    def get_order(self, order_id):
        order = self.db.run(("""SELECT * FROM orders WHERE
                                order_id = %s""",), (order_id,), 'SELECT')
        return order

    def update_order(self, order_id, status):
        updated = self.db.run(("""UPDATE orders SET status = %s
                                WHERE order_id = %s""",),
                              (status, order_id,), 'UPDATE')
        return updated

    def delete_order(self, order_id):
        self.db.run(("""DELETE FROM orders WHERE
                      order_id = %s""",), (order_id,))
        return 'Order successfully deleted.'

    def get_orders(self):
        orders = self.db.run(("""SELECT * FROM orders""",), command='SELECT')
        return orders
