from API.models import Users, Orders, Menu
from API.db import Database
from API.routes import app
from API.validation import Check

if __name__ == '__main__':
    """u = {'name': 'rice', 'price': '2000', 'status': 'Available',
         'tags': 'meal'}
    m = Menu().get_menu()
    print(m)"""
    app.run(debug=True)
