import unittest
import json
from module.routes import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    # Helper methods
    def place_order(self):
        response = self.app.post('/api/v1/orders', data=json.dumps({'name\
': 'Pizza', 'quantity': 1, 'time': '1 hr', 'user_id': 1, 'location': 'Buko\
to'}), content_type='application/json')
        return response

    def update_order(self, l):
        response = self.app.put('/api/v1/orders/1', data=json.dumps({'status\
': "{}".format(l)}), content_type='application/json')
        return response

    def test_place_order(self):
        response = self.place_order()
        self.assertEqual('Your order was successfully placed. Order Id: \
3', response.json)

    def partial_content(self):
        response = self.app.post('/api/v1/orders', data=json.dumps({'name\
': 'Pizza', 'time': '1 hr', 'user_id': 1, 'location': 'Buko\
to'}), content_type='application/json')
        return response

    def get_order(self):
        response = self.app.get('/api/v1/orders/1')
        return response

    def get_order_not_found(self):
        response = self.app.get('/api/v1/orders/3')
        return response

    def update_order_not_found(self):
        response = self.app.put('/api/v1/orders/5', data=json.dumps({'status\
': "P"}), content_type='application/json')
        return response

    def all_orders(self):
        response = self.app.get('/api/v1/orders')
        return response
    # End helper functions

    def test_place_order_status_code(self):
        response = self.place_order()
        self.assertEqual(200, response.status_code)

    def test_partial_content(self):
        response = self.partial_content()
        self.assertEqual('You must provide all required values. [name, quantity,\
time, user_id, location]', response.json)

    def test_partial_content_status_code(self):
        response = self.partial_content()
        self.assertEqual(206, response.status_code)

    def test_get_order(self):
        self.place_order()
        response = self.get_order()
        self.assertEqual({"id": 1, "name": "Pizza", "quantity": 1, "wanted_in": "1 hr\
", "requester": 1, "status": "Queued", "where": "Bukoto"}, response.json)

    def test_get_order_status_code(self):
        self.place_order()
        response = self.get_order()
        self.assertEqual(200, response.status_code)

    def test_get_order_not_found(self):
        response = self.get_order_not_found()
        self.assertEqual('Order with Id: 3 not found.', response.json)

    def test_get_order_not_found_status_code(self):
        response = self.get_order_not_found()
        self.assertEqual(404, response.status_code)

    def test_update_order_to_pending(self):
        response = self.update_order('P')
        self.assertEqual('Your order was successfully updated. Order Id: \
1', response.json)

    def test_update_order_to_declined(self):
        response = self.update_order('D')
        self.assertEqual('Your order was successfully updated. Order Id: \
1', response.json)

    def test_update_order_to_completed(self):
        response = self.update_order('C')
        self.assertEqual('Your order was successfully updated. Order Id: \
1', response.json)

    def test_update_order_to_undefined(self):
        response = self.update_order('z')
        self.assertEqual('Your order was successfully updated. Order Id: \
1', response.json)

    def test_update_order_not_found(self):
        response = self.update_order_not_found()
        self.assertEqual('Order with Id: 5 not found.', response.json)

    def test_update_order_not_found_status_code(self):
        response = self.update_order_not_found()
        self.assertEqual(404, response.status_code)

    def test_update_order_no_content(self):
        response = self.app.put('/api/v1/orders/1', data=json.dumps({}),
                                content_type='application/json')
        self.assertEqual('You must provide the required value. [status]',
                         response.json)

    def test_all_orders(self):
        response = self.all_orders()
        self.assertEqual([], response.json)

    def test_all_orders_status_code(self):
        response = self.all_orders()
        self.assertEqual(200, response.status_code)
