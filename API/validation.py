from flask import jsonify
from API.db import Database


class Check:

    def __init__(self):
        from API.routes import app
        self.db = Database(app)

    def is_clean(self, container):

        new_container = {}
        try:
            for key in container:
                value = str(container[key]).strip(' ')
                if value == '':
                    raise KeyError
                else:
                    new_container[key] = value
        except KeyError:
            return jsonify('[{}] is empty.'.format(key)), 400
        return new_container

    def unwrap(self, container):
        if len(container) == 1:
            for item in container:
                return item

        else:
            pass

    def is_admin(self, user_id):
        response = self.db.run(("""SELECT role FROM Users WHERE
                                user_id = %s""",),
                               (user_id,), 'SELECT')
        role = self.unwrap(response)
        print(role)
        if role[0] == 'Admin':
            return True
        else:
            return False

    def user_exists(self, user_id):
        response = self.db.run(("""SELECT * FROM Users WHERE
                                user_id = %s""",),
                               (user_id,), 'SELECT')
        user = Check().unwrap(response)
        return user

    def food_exists(self, food_id):
        response = self.db.run(("""SELECT * FROM Menu WHERE
                                user_id = %s""",),
                               (food_id,), 'SELECT')
        food = Check().unwrap(response)
        return food

