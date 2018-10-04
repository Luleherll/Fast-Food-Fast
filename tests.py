import unittest
import json
from API.routes import app
from API.db import Database


class TestUsers(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        self.db = Database(app)

    @classmethod
    def tearDown(self):
        self.db.clean_tables()

    def test_register_user(self):
        response = self.app.post('/api/v2/auth/signup', data=json.dumps(
            {'username': 'tog', 'password': 'dal', 'tel': '0999',
             'email': 'tom@dev.com', 'location': 'some', 'key point': 'hhh'}),
            content_type='application/json')
        self.assertEqual('Signup successful. You can login now.',
                         response.json)
        self.assertEqual(201, response.status_code)

    def test_register_user_exists(self):
        self.app.post('/api/v2/auth/signup', data=json.dumps(
            {'username': 'tol', 'password': 'dal', 'tel': '0999',
             'email': 'tom@dev.com', 'location': 'some', 'key point': 'hhh'}),
            content_type='application/json')
        response = self.app.post('/api/v2/auth/signup', data=json.dumps(
            {'username': 'tol', 'password': 'dal', 'tel': '0999',
             'email': 'tom@dev.com', 'location': 'some', 'key point': 'hhh'}),
            content_type='application/json')
        self.assertEqual('User named tol already exists.', response.json)
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
             'email': 'tom@dev.com', 'location': '' ,'key point': 'hhh'}),
            content_type='application/json')
        self.assertEqual('[location] is empty.', response.json)
        self.assertEqual(400, response.status_code)

    def test_login(self):
        response = self.app.post('/api/v2/auth/login', data=json.dumps(
            {'username': 'tol', 'password': 'dal'}),
             content_type='application/json')
        self.assertIn(b'access_token', response.data)
        self.assertEqual(200, response.status_code)

    def test_login_unregistered(self):
        response = self.app.post('/api/v2/auth/login', data=json.dumps(
            {'username': 'tolx', 'password': 'dalx'}),
             content_type='application/json')
        self.assertIn(b'access_token', response.data)
        self.assertEqual(200, response.status_code)


"""class TestOrders(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.helper = Helper(self.app)

    def test_place_order(self):
        response = self.helper.place_order(20, 'fill', 'lule')
        self.assertEqual('Your order was successfully placed. Order Id: \
2', response.json)
        self.assertEqual(201, response.status_code)

    def test_place_order_partial_content(self):
        response = self.helper.partial_content()
        self.assertEqual('You must provide the required values. [name, quantity,\
 comment, username]', response.json)
        self.assertEqual(400, response.status_code)

    def test_place_order_ValueError(self):
        response = self.helper.place_order('a', 'fill', 'lule')
        self.assertEqual('The server encountered an error which is due\
 to an invalid data type. Valid format: [letters,numbers,letters,\
letters]', response.json)
        self.assertEqual(400, response.status_code)

    def test_place_order_AttributeError(self):
        response = self.helper.place_order(1, 2, 'lule')
        self.assertEqual('The server encountered an error which is due\
 to an invalid data type. Valid format: [letters,numbers,letters,\
letters]', response.json)
        self.assertEqual(400, response.status_code)

    def test_place_order_empty(self):
        response = self.helper.place_order(2, '', 'lule')
        self.assertEqual('You must fill in all the fields.',
                         response.json)
        self.assertEqual(400, response.status_code)

    def test_get_order(self):
        self.helper.place_order(1, 'hurry.', 'lule')
        response = self.helper.get_order()
        self.assertEqual({"id": 1, "name": "Pizza", "quantity": 1, "comment": "hurry.\
", "requester": 'lule', "status": "Queued", "where": "Kasubi"}, response.json)
        self.assertEqual(200, response.status_code)

    def test_get_order_not_found(self):
        response = self.helper.get_order_not_found()
        self.assertEqual('Order with Id: 3 not found.', response.json)
        self.assertEqual(404, response.status_code)

    def test_update_order_to_pending(self):
        response = self.helper.update_order('Pending')
        self.assertEqual('Your order was successfully updated. Order Id: \
1', response.json)

    def test_update_order_to_declined(self):
        response = self.helper.update_order('Declined')
        self.assertEqual('Your order was successfully updated. Order Id: \
1', response.json)

    def test_update_order_to_completed(self):
        response = self.helper.update_order('Completed')
        self.assertEqual('Your order was successfully updated. Order Id: \
1', response.json)

    def test_update_order_to_undefined(self):
        response = self.helper.update_order('zoo')
        self.assertEqual("The status you provided is invalid. Choose from \
['Queued', 'Pending', 'Declined', 'Completed']", response.json)
        self.assertEqual(400, response.status_code)

    def test_update_to_number(self):
        response = self.helper.update_order(1)
        self.assertEqual('The server encountered an error which is due\
 to an invalid data type. Valid format: [letters]', response.json)

    def test_update_to_empty(self):
        response = self.helper.update_order('')
        self.assertEqual('You must fill in all the fields.', response.json)

    def test_update_order_not_found(self):
        response = self.helper.update_order_not_found()
        self.assertEqual('Order with Id: 5 not found.', response.json)
        self.assertEqual(404, response.status_code)

    def test_update_order_no_content(self):
        response = self.app.put('/api/v1/orders/1', data=json.dumps({}),
                                content_type='application/json')
        self.assertEqual('You must provide the required values. [status]',
                         response.json)

    def test_all_orders(self):
        response = self.helper.all_orders()
        self.assertEqual([], response.json)
        self.assertEqual(200, response.status_code)

    def test_welcome(self):
        response = self.app.get('/')
        self.assertEqual('Welcome to the Fast-Food-Fast API', response.json)

    def test_page_not_found(self):
        response = self.app.get('/api/orders')
        self.assertEqual(b"<h1>You're lost in the woods:<br> Go back to index:<h1>\
<a href='https://lule-fast-food.herokuapp.com/'>Click Here<a>", response.data)


class TestFoodList(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.helper = Helper(self.app)

    def test_add_food_item(self):
        response = self.helper.add_food_item('fries', 20)
        self.assertEqual('[fries] added successfully.', response.json)
        self.assertEqual(201, response.status_code)

    def test_add_food_ValueError(self):
        response = self.helper.add_food_item('fries', 'a')
        self.assertEqual('The server encountered an error which is due\
 to an invalid data type. Valid format: [letters,numbers,letters for all\
 the rest]', response.json)

    def test_add_food_item_AttributeError(self):
        response = self.helper.add_food_item(1, 20)
        self.assertEqual('The server encountered an error which is due\
 to an invalid data type. Valid format: [letters,numbers,letters for all\
 the rest]', response.json)

    def test_add_food_item_empty(self):
        response = self.helper.add_food_item('', 20)
        self.assertEqual('You must fill in all the fields.',
                         response.json)

    def test_add_food_item_partial_content(self):
        response = self.helper.add_food_item_partial()
        self.assertEqual('You must provide the required values. [name,\
 price, ready in, status, units, tags', response.json)
        self.assertEqual(400, response.status_code)

    def test_add_food_item_exists(self):
        response = self.helper.add_food_item('fries', 20)
        self.assertEqual('Food with name: fries already exists. Try upd\
ating.', response.json)
        self.assertEqual(403, response.status_code)

    def test_update_food_item(self):
        response = self.helper.add_food_item('fries', 20)
        response = self.helper.update_food_item('fries')
        self.assertEqual('[fries] updated successfully.', response.json)
        self.assertEqual(202, response.status_code)

    def test_update_food_item_not_exist(self):
        response = self.helper.update_food_item('buns')
        self.assertEqual('Food with name: buns not found in food list\
', response.json)
        self.assertEqual(404, response.status_code)

    def test_delete_food_item(self):
        response = self.helper.delete_food_item('fries')
        self.assertEqual('[fries] deleted successfully.', response.json)
        self.assertEqual(200, response.status_code)

    def test_delete_food_item_not_exist(self):
        response = self.helper.delete_food_item('bans')
        self.assertEqual('Food with name: bans not found in food list\
', response.json)
        self.assertEqual(404, response.status_code)

    def test_get_menu(self):
        response = self.helper.get_menu()
        self.assertEqual({}, response.json)
        self.assertEqual(200, response.status_code)"""
