from API.models import Users, Orders, Menu
from API.db import Database
from API.routes import app
from API.validation import Check

if __name__ == '__main__':
    u = {'username': 'lule', 'password': 'dev', 'tel': '07777',
         'email': 'lule@dev.com', 'location': 'Nalya',
         'key_point': 'Acacia mall entrance'}
    """x = Users().register(u)
    print(x)"""
    y = {'name': 'rice', 'status': 'Available',
         'tags': '  meal  '}
    x = {'user_id': '17', 'food_id': '2', 'name': 'rice',
         'quantity': '2', 'comment': 'hurry',
         'location': 'Nalya', 'amount': '4000'}
    m = Check().clean(y)
    print(m)

