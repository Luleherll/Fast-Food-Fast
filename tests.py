import unittest
import json
from module.routes import app


class Helper:
    "This class contains methods used for testing."
    def __init__(self, arg):
        self.arg = arg

    # Methods for TestOrders class
    def place_order(self):
        response = self.arg.post('/api/v1/orders', data=json.dumps({'name\
': 'Pizza', 'quantity': 1, 'time': '1 hr', 'user_id': 1, 'location': 'Buko\
to'}), content_type='application/json')
        return response

    def update_order(self, l):
        response = self.arg.put('/api/v1/orders/1', data=json.dumps({'status\
': "{}".format(l)}), content_type='application/json')
        return response

    def partial_content(self):
        response = self.arg.post('/api/v1/orders', data=json.dumps({'name\
': 'Pizza', 'time': '1 hr', 'user_id': 1, 'location': 'Buko\
to'}), content_type='application/json')
        return response

    def get_order(self):
        response = self.arg.get('/api/v1/orders/1')
        return response

    def get_order_not_found(self):
        response = self.arg.get('/api/v1/orders/3')
        return response

    def update_order_not_found(self):
        response = self.arg.put('/api/v1/orders/5', data=json.dumps({'status\
': "P"}), content_type='application/json')
        return response

    def all_orders(self):
        response = self.arg.get('/api/v1/orders')
        return response
    # End of TestOrders methods

    # Methods of TestFoodList class
    def add_food_item(self, name):
        response = self.arg.post('/api/v1/menu/add', data=json.dumps({'name\
': '{}'.format(name), "price": 5000, 'ready in': '30 mins', 'status': 'Avai\
lable', 'units': 'plate', 'tags': 'snack'}), content_type='application/json')
        return response

    def add_food_item_partial(self):
        response = self.arg.post('/api/v1/menu/add', data=json.dumps({'name\
': 'pizza', 'ready in': '30 mins', 'status': 'Avai\
lable', 'units': 'plate', 'tags': 'snack'}), content_type='application/json')
        return response

    def update_food_item(self, name):
        response = self.arg.put('/api/v1/menu/{}'.format(name),
                                data=json.dumps({"price": 6000, 'status': '\
Unavailable'}), content_type='application/json')
        return response

    def delete_food_item(self, name):
        response = self.arg.delete('/api/v1/menu/{}'.format(name))
        return response

    def get_menu(self):
        response = self.arg.get('/api/v1/menu')
        return response
    # End of TestFoodList methods


class TestOrders(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.helper = Helper(self.app)

    def test_place_order(self):
        response = self.helper.place_order()
        self.assertEqual('Your order was successfully placed. Order Id: \
3', response.json)

    def test_place_order_status_code(self):
        response = self.helper.place_order()
        self.assertEqual(200, response.status_code)

    def test_partial_content(self):
        response = self.helper.partial_content()
        self.assertEqual('You must provide the required values. [name, quantity,\
 time, user_id, location]', response.json)

    def test_partial_content_status_code(self):
        response = self.helper.partial_content()
        self.assertEqual(206, response.status_code)

    def test_get_order(self):
        self.helper.place_order()
        response = self.helper.get_order()
        self.assertEqual({"id": 1, "name": "Pizza", "quantity": 1, "wanted_in": "1 hr\
", "requester": 1, "status": "Queued", "where": "Bukoto"}, response.json)

    def test_get_order_status_code(self):
        self.helper.place_order()
        response = self.helper.get_order()
        self.assertEqual(200, response.status_code)

    def test_get_order_not_found(self):
        response = self.helper.get_order_not_found()
        self.assertEqual('Order with Id: 3 not found.', response.json)

    def test_get_order_not_found_status_code(self):
        response = self.helper.get_order_not_found()
        self.assertEqual(404, response.status_code)

    def test_update_order_to_pending(self):
        response = self.helper.update_order('P')
        self.assertEqual('Your order was successfully updated. Order Id: \
1', response.json)

    def test_update_order_to_declined(self):
        response = self.helper.update_order('D')
        self.assertEqual('Your order was successfully updated. Order Id: \
1', response.json)

    def test_update_order_to_completed(self):
        response = self.helper.update_order('C')
        self.assertEqual('Your order was successfully updated. Order Id: \
1', response.json)

    def test_update_order_to_undefined(self):
        response = self.helper.update_order('z')
        self.assertEqual('Your order was successfully updated. Order Id: \
1', response.json)

    def test_update_order_not_found(self):
        response = self.helper.update_order_not_found()
        self.assertEqual('Order with Id: 5 not found.', response.json)

    def test_update_order_not_found_status_code(self):
        response = self.helper.update_order_not_found()
        self.assertEqual(404, response.status_code)

    def test_update_order_no_content(self):
        response = self.app.put('/api/v1/orders/1', data=json.dumps({}),
                                content_type='application/json')
        self.assertEqual('You must provide the required values. [status]',
                         response.json)

    def test_all_orders(self):
        response = self.helper.all_orders()
        self.assertEqual([], response.json)

    def test_all_orders_status_code(self):
        response = self.helper.all_orders()
        self.assertEqual(200, response.status_code)

    def test_welcome(self):
        response = self.app.get('/')
        self.assertEqual(b'<h1>Welcome to the Fast-Food-Fast API<h1>\
', response.data)


class TestFoodList(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.helper = Helper(self.app)

    def test_add_food_item(self):
        response = self.helper.add_food_item('fries')
        self.assertEqual('[fries] added successfully.', response.json)

    def test_add_food_item_partial_content(self):
        response = self.helper.add_food_item_partial()
        self.assertEqual('You must provide the required values. [name,\
 price, ready in, status, units, tags', response.json)

    def test_add_food_item_partial_content_status_code(self):
        response = self.helper.add_food_item_partial()
        self.assertEqual(206, response.status_code)

    def test_add_food_item_status_code(self):
        response = self.helper.add_food_item('pizza')
        self.assertEqual(200, response.status_code)

    def test_add_food_item_exists(self):
        response = self.helper.add_food_item('fries')
        self.assertEqual('Food with name: fries already exists. Try upd\
ating.', response.json)

    def test_add_food_item_exists_status_code(self):
        response = self.helper.add_food_item('fries')
        self.assertEqual(501, response.status_code)

    def test_update_food_item(self):
        response = self.helper.update_food_item('fries')
        self.assertEqual('[fries] updated successfully.', response.json)

    def test_update_food_item_status_code(self):
        response = self.helper.update_food_item('fries')
        self.assertEqual(200, response.status_code)

    def test_update_food_item_not_exist(self):
        response = self.helper.update_food_item('bans')
        self.assertEqual('Food with name: bans not found in food list\
', response.json)

    def test_update_food_item_not_exist_status_code(self):
        response = self.helper.update_food_item('bans')
        self.assertEqual(404, response.status_code)

    def test_delete_food_item(self):
        self.helper.add_food_item('pancakes')
        response = self.helper.delete_food_item('pancakes')
        self.assertEqual('[pancakes] deleted successfully.', response.json)

    def test_delete_food_item_status_code(self):
        response = self.helper.delete_food_item('pizza')
        self.assertEqual(200, response.status_code)

    def test_delete_food_item_not_exist(self):
        response = self.helper.delete_food_item('bans')
        self.assertEqual('Food with name: bans not found in food list\
', response.json)

    def test_delete_food_item_not_exist_status_code(self):
        response = self.helper.delete_food_item('bans')
        self.assertEqual(404, response.status_code)

    def test_get_menu(self):
        response = self.helper.get_menu()
        self.assertEqual({'fries': {'name': 'fries', 'price\
': 5000, 'ready in': '30 mins', 'status': 'Available', 'tags': 'snack\
', 'units': 'plate'}}, response.json)

    def test_get_menu_status_code(self):
        response = self.helper.get_menu()
        self.assertEqual(200, response.status_code)
