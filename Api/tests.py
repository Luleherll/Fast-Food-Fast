import unittest
import json
from module.routes import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_place_order(self):
        response = self.app.post('/api/v1/orders', data=json.dumps({'name\
': 'Pizza', 'quantity': 1, 'time': '1 hr', 'user_id': 1, 'location': 'Buko\
to'}), content_type='application/json')
        self.assertEqual('Your order was successfully placed. Order Id: \
3', response.json)

    def test_place_order_status_code(self):
        response = self.app.post('/api/v1/orders', data=json.dumps({'name\
': 'Pizza', 'quantity': 1, 'time': '1 hr', 'user_id': 1, 'location': 'Buko\
to'}), content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_partial_content(self):
        response = self.app.post('/api/v1/orders', data=json.dumps({'name\
': 'Pizza', 'time': '1 hr', 'user_id': 1, 'location': 'Buko\
to'}), content_type='application/json')
        self.assertEqual('You must provide all required values. [name, quantity,\
time, user_id, location]', response.json)

    def test_partial_content_status_code(self):
        response = self.app.post('/api/v1/orders', data=json.dumps({'name\
': 'Pizza', 'time': '1 hr', 'user_id': 1, 'location': 'Buko\
to'}), content_type='application/json')
        self.assertEqual(206, response.status_code)

    def test_get_order(self):
        self.app.post('/api/v1/orders', data=json.dumps({'name\
': 'Pizza', 'quantity': 1, 'time': '1 hr', 'user_id': 1, 'location': 'Buko\
to'}), content_type='application/json')
        response = self.app.get('/api/v1/orders/1')
        self.assertEqual({"id": 1, "name": "Pizza", "quantity": 1, "wanted_in": "1 hr\
", "requester": 1, "status": "Queued", "where": "Bukoto"}, response.json)

    def test_get_order_status_code(self):
        self.app.post('/api/v1/orders', data=json.dumps({'name\
': 'Pizza', 'quantity': 1, 'time': '1 hr', 'user_id': 1, 'location': 'Buko\
to'}), content_type='application/json')
        response = self.app.get('/api/v1/orders/1')
        self.assertEqual(200, response.status_code)

    def test_get_order_not_found(self):
        response = self.app.get('/api/v1/orders/3')
        self.assertEqual('Order with Id: 3 not found.', response.json)

    def test_get_order_not_found_status_code(self):
        response = self.app.get('/api/v1/orders/3', data=json.dumps({'status\
': "P"}), content_type='application/json')
        self.assertEqual(404, response.status_code)

    def test_update_order_to_pending(self):
        response = self.app.put('/api/v1/orders/1', data=json.dumps({'status\
': "P"}), content_type='application/json')
        self.assertEqual('Your order was successfully updated. Order Id: \
1', response.json)

    def test_update_order_to_declined(self):
        response = self.app.put('/api/v1/orders/1', data=json.dumps({'status\
': "D"}), content_type='application/json')
        self.assertEqual('Your order was successfully updated. Order Id: \
1', response.json)

    def test_update_order_to_completed(self):
        response = self.app.put('/api/v1/orders/1', data=json.dumps({'status\
': "C"}), content_type='application/json')
        self.assertEqual('Your order was successfully updated. Order Id: \
1', response.json)

    def test_update_order_to_undefined(self):
        response = self.app.put('/api/v1/orders/1', data=json.dumps({'status\
': "z"}), content_type='application/json')
        self.assertEqual('Your order was successfully updated. Order Id: \
1', response.json)

    def test_update_order_not_found(self):
        response = self.app.put('/api/v1/orders/5', data=json.dumps({'status\
': "P"}), content_type='application/json')
        self.assertEqual('Order with Id: 5 not found.', response.json)

    def test_update_order_not_found_status_code(self):
        response = self.app.put('/api/v1/orders/5', data=json.dumps({'status\
': "P"}), content_type='application/json')
        self.assertEqual(404, response.status_code)

    def test_update_order_no_content(self):
        response = self.app.put('/api/v1/orders/1', data=json.dumps({}),
                                content_type='application/json')
        self.assertEqual('You must provide the required value. [status]',
                         response.json)

    def test_all_orders(self):
        response = self.app.get('/api/v1/orders')
        self.assertEqual([], response.json)

    def test_all_orders_status_code(self):
        response = self.app.get('/api/v1/orders')
        self.assertEqual(200, response.status_code)
