from API.models import Users, Orders, Menu
from API.db import Database
from API.routes import app
from API.validation import Check

if __name__ == '__main__':
    Database
    app.run(debug=True)
