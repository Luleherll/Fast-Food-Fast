from API.models import Users, Orders, Menu
from API.db import Database
from API.routes import app
from API.validation import Check

if __name__ == '__main__':
    d = Database(app)
    d.create_tables
    app.run(debug=True)
