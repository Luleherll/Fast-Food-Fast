import unittest
import json
from API.routes import app
from API.db import Database


def get_token(app):
    token = app.post('/api/v2/auth/login', data=json.dumps(
            {'username': 'tanner', 'password': 'pass'}),
             content_type='application/json')
    data = json.loads(token.data.decode())
    return data


class TestApi(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        self.db = Database(app)
        m = self.db.create_tables()
        print(m)

    def tearDown(self):
        r = self.db.drop_tables()
        print(r)

    def test_register_user(self):
        response = self.app.post('/api/v2/auth/signup', data=json.dumps(
            {'username': 'sanner', 'password': 'dal', 'tel': '0999',
             'email': 'tom@dev.com', 'location': 'some', 'key point': 'hhh'}),
            content_type='application/json')
        
        self.assertEqual({'msg': 'Signup successful. You can login now.'},
                         response.json)
        self.assertEqual(201, response.status_code)

    def test_register_user_exists(self):
        response = self.app.post('/api/v2/auth/signup', data=json.dumps(
            {'username': 'tanner', 'password': 'dal', 'tel': '0999',
             'email': 'tom@dev.com', 'location': 'some', 'key point': 'hhh'}),
            content_type='application/json')
        self.assertEqual({'msg': 'User named tanner already exists.'}, response.json)
        self.assertEqual(406, response.status_code)

    def test_register_user_partial(self):
        response = self.app.post('/api/v2/auth/signup', data=json.dumps(
            {'username': 'tol', 'password': 'dal', 'tel': '0999',
             'email': 'tom@dev.com', 'key point': 'hhh'}),
            content_type='application/json')
        self.assertEqual({'error': 'You must provide all required fields.'},
                         response.json)
        self.assertEqual(400, response.status_code)

    def test_register_user_empty_field(self):
        response = self.app.post('/api/v2/auth/signup', data=json.dumps(
            {'username': 'tol', 'password': 'dal', 'tel': '0999',
             'email': 'tom@dev.com', 'location': '', 'key point': 'hhh'}),
            content_type='application/json')
        self.assertEqual({'msg': '[location] is empty.'}, response.json)
        self.assertEqual(400, response.status_code)

    def test_login(self):
        response = self.app.post('/api/v2/auth/login', data=json.dumps(
            {'username': 'tanner', 'password': 'pass'}),
             content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_login_unregistered(self):
        response = self.app.post('/api/v2/auth/login', data=json.dumps(
            {'username': 'tolx', 'password': 'dalx'}),
             content_type='application/json')
        self.assertEqual({'error': 'Not Registered.'}, response.json)
        self.assertEqual(401, response.status_code)

    def test_login_empty(self):
        response = self.app.post('/api/v2/auth/login', data=json.dumps(
            {'username': '', 'password': 'dalx'}),
             content_type='application/json')
        self.assertEqual({'msg': '[username] is empty.'}, response.json)
        self.assertEqual(400, response.status_code)

    def test_login_partial(self):
        response = self.app.post('/api/v2/auth/login', data=json.dumps(
            {'password': 'dalx'}),
             content_type='application/json')
        self.assertEqual({'error': 'You must provide all required fields.'},
                         response.json)
        self.assertEqual(400, response.status_code)  

    def test_get_menu(self):
        token = get_token(self.app)
        response = self.app.get('/api/v2/menu', headers={'Authorization':
                                'Bearer {}'.format(token)})
        self.assertEqual([{'food_id': 1, 'img1': 'tanner.jpg',
                           'img2': 'tanne.jpg', 'img3': 'tann.jpg',
                           'name': 'coveralls', 'price': 1000,
                           'status': 'Available', 'tags': 'meal'}],
                         response.json)
        self.assertEqual(200, response.status_code)

    def test_update_menu(self):
        token = get_token(self.app)
        response = self.app.put('/api/v2/menu', data=json.dumps(
                           {'food_id': 1, 'img1': 'tanner.jpg',
                            'img2': 'tanne.jpg', 'img3': 'tann.jpg',
                            'name': 'coveralls', 'price': 1000,
                            'status': 'Unavailable', 'tags': 'meal'}),
                            content_type='application/json', headers={'Authorization':
                             'Bearer {}'.format(token)})
        self.assertEqual({'msg': 'Food updated successfully.'},
                         response.json)
        self.assertEqual(200, response.status_code)

    def test_make_admin(self):
        token = get_token(self.app)
        self.app.post('/api/v2/auth/signup', data=json.dumps(
            {'username': 'banner', 'password': 'dal', 'tel': '0999',
             'email': 'banner@dev.com', 'location': 'some', 'key point': 'hhh'}),
            content_type='application/json')
        response = self.app.put('/api/v2/auth/admin', data=json.dumps(
            {'username': 'banner'}), content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual({'msg': 'banner made administrator.'}, response.json)

    def test_make_order(self):
        token = get_token(self.app)

        response = self.app.post('/api/v2/users/orders', data=json.dumps(
            {'name': 'coveralls', 'quantity': 2, 'comment': 'hurry'}),
             content_type='application/json', headers={'Authorization':
             'Bearer {}'.format(token)})
        self.assertEqual({'msg': 'Your order was placed successfully.'},
                         response.json)
        self.assertEqual(201, response.status_code)

    def test_make_order_food_not_exist(self):
        token = get_token(self.app)
        response = self.app.post('/api/v2/users/orders', data=json.dumps(
            {'name': 'cassava', 'quantity': 2, 'comment': 'hurry'}),
             content_type='application/json', headers={'Authorization':
                                 'Bearer {}'.format(token)})
        self.assertEqual({'msg': 'Food name you specified is not found.'},
                         response.json)
        self.assertEqual(404, response.status_code)

    def test_get_user_orders(self):
        token = get_token(self.app)
        response = self.app.get('/api/v2/users/orders', headers={'Authorization':
                                'Bearer {}'.format(token)})
        self.assertEqual([], response.json)
        self.assertEqual(200, response.status_code)

    def test_get_pending_orders(self):
        token = get_token(self.app)
        response = self.app.get('/api/v2/orders/pending', headers={'Authorization':
                                'Bearer {}'.format(token)})
        self.assertEqual([], response.json)
        self.assertEqual(200, response.status_code)

    def test_get_archived_orders(self):
        token = get_token(self.app)
        response = self.app.get('/api/v2/orders/archive', headers={'Authorization':
                                'Bearer {}'.format(token)})
        self.assertEqual([], response.json)
        self.assertEqual(200, response.status_code)

    def test_get_user_history(self):
        token = get_token(self.app)
        response = self.app.get('/api/v2/users/history', headers={'Authorization':
                                'Bearer {}'.format(token)})
        self.assertEqual([], response.json)
        self.assertEqual(200, response.status_code)

    def test_get_orders(self):
        token = get_token(self.app)
        response = self.app.get('/api/v2/orders/', headers={'Authorization':
                                'Bearer {}'.format(token)})
        self.assertEqual([], response.json)
        self.assertEqual(200, response.status_code)

    def test_not_found(self):
        response = self.app.get('/api/v2/users/orderss')
        self.assertEqual(b"<h1>You're lost in the woods:<br> Go back to index:<h1>\
<a href='https://lule-persistent.herokuapp.com/'>Click Here<a>", response.data)
        self.assertEqual(404, response.status_code)


