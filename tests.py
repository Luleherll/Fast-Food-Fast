import unittest
import json
from API.routes import app
from API.db import Database


def get_token(app):
    token = app.post('/api/v2/auth/login', data=json.dumps(
            {'username': 'tanner', 'password': 'dal'}),
             content_type='application/json')
    data = json.loads(token.data.decode())
    return data


class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        self.db = Database(app)
        self.db.clean_tables()
        self.db.create_tables()
        self.app.post('/api/v2/auth/signup', data=json.dumps(
            {'username': 'tanner', 'password': 'dal', 'tel': '0999',
             'email': 'tom@dev.com', 'location': 'sme', 'key point': 'hhh'}),
            content_type='application/json')

    @classmethod
    def tearDownClass(self):
        self.db.clean_tables()

    def test_register_user(self):
        response = self.app.post('/api/v2/auth/signup', data=json.dumps(
            {'username': 'banner', 'password': 'dal', 'tel': '0999',
             'email': 'tom@dev.com', 'location': 'some', 'key point': 'hhh'}),
            content_type='application/json')
        self.assertEqual('Signup successful. You can login now.',
                         response.json)
        self.assertEqual(201, response.status_code)

    def test_register_user_exists(self):
        """self.app.post('/api/v2/auth/signup', data=json.dumps(
            {'username': '', 'password': 'dal', 'tel': '0999',
             'email': 'tom@dev.com', 'location': 'some', 'key point': 'hhh'}),
            content_type='application/json')"""
        response = self.app.post('/api/v2/auth/signup', data=json.dumps(
            {'username': 'tanner', 'password': 'dal', 'tel': '0999',
             'email': 'tom@dev.com', 'location': 'some', 'key point': 'hhh'}),
            content_type='application/json')
        self.assertEqual('User named tanner already exists.', response.json)
        self.assertEqual(406, response.status_code)

    def test_register_user_partial(self):
        response = self.app.post('/api/v2/auth/signup', data=json.dumps(
            {'username': 'tol', 'password': 'dal', 'tel': '0999',
             'email': 'tom@dev.com', 'key point': 'hhh'}),
            content_type='application/json')
        self.assertEqual('Missing data', response.json)
        self.assertEqual(400, response.status_code)

    def test_register_user_empty_field(self):
        response = self.app.post('/api/v2/auth/signup', data=json.dumps(
            {'username': 'tol', 'password': 'dal', 'tel': '0999',
             'email': 'tom@dev.com', 'location': '' , 'key point': 'hhh'}),
            content_type='application/json')
        self.assertEqual('[location] is empty.', response.json)
        self.assertEqual(400, response.status_code)

    def test_login(self):
        response = self.app.post('/api/v2/auth/login', data=json.dumps(
            {'username': 'tanner', 'password': 'dal'}),
             content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_login_unregistered(self):
        response = self.app.post('/api/v2/auth/login', data=json.dumps(
            {'username': 'tolx', 'password': 'dalx'}),
             content_type='application/json')
        self.assertIn('Not Registered.', response.json)
        self.assertEqual(401, response.status_code)

    def test_login_partial(self):
        response = self.app.post('/api/v2/auth/login', data=json.dumps(
            {'username': '', 'password': 'dalx'}),
             content_type='application/json')
        self.assertEqual('[username] is empty.', response.json)
        self.assertEqual(400, response.status_code)

    def test_get_menu(self):
        token = get_token(self.app)
        response = self.app.get('/api/v2/menu', headers={'Authorization':
                                'Bearer {}'.format(token)})
        self.assertEqual({}, response.json)
        self.assertEqual(200, response.status_code)

    def test_make_admin(self):
        d = self.app.post('/api/v2/auth/signup', data=json.dumps(
            {'username': 'tanner', 'password': 'dal', 'tel': '0999',
             'email': 'tom@dev.com', 'location': 'sme', 'key point': 'hhh'}),
            content_type='application/json')
        token = get_token(self.app)
        response = self.app.post('/api/v2/auth/admin', data=json.dumps(
            {'username': 'tanner'}), content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual('tanner made administrator.', response.json)

    def test_make_order(self):
        token = get_token(self.app)
        self.app.post('/api/v2/menu', data=json.dumps(
            {'name': 'meat', 'price': '1000', 'status': 'Available',
             'tags': 'meal'}), content_type='application/json',
             headers={'Authorization': 'Bearer {}'.format(token)})
        response = self.app.post('/api/v2/users/orders', data=json.dumps(
            {'name': 'meat', 'quantity': 2, 'comment': 'hurry'}),
             content_type='application/json', headers={'Authorization':
                                 'Bearer {}'.format(token)})
        self.assertEqual('Your order was placed successfully.', response.json)
        self.assertEqual(201, response.status_code)

    def test_make_order_food_not_exist(self):
        token = get_token(self.app)
        response = self.app.post('/api/v2/users/orders', data=json.dumps(
            {'name': 'cassava', 'quantity': 2, 'comment': 'hurry'}),
             content_type='application/json', headers={'Authorization':
                                 'Bearer {}'.format(token)})
        self.assertEqual('Food name you specified is not found.', response.json)
        self.assertEqual(404, response.status_code)

    def test_get_history(self):
        token = get_token(self.app)
        response = self.app.get('/api/v2/users/orders', headers={'Authorization':
                                'Bearer {}'.format(token)})
        self.assertEqual({}, response.json)
        self.assertEqual(200, response.status_code)

    def test_not_found(self):
        token = get_token(self.app)
        response = self.app.get('/api/v2/users/orderss', headers={'Authorization':
                                'Bearer {}'.format(token)})
        self.assertEqual(b"<h1>You're lost in the woods:<br> Go back to index:<h1>\
<a href='https://lule-persistent.herokuapp.com/'>Click Here<a>", response.data)
        self.assertEqual(404, response.status_code)

    def test_welcome_page(self):
        token = get_token(self.app)
        response = self.app.get('/', headers={'Authorization':
                                'Bearer {}'.format(token)})
        self.assertEqual(b'"Welcome to the Fast-Food-Fast API"\n', response.data)
        self.assertEqual(200, response.status_code)

