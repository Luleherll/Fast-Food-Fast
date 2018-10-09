import psycopg2 as pg


class Database:

    def __init__(self, app):
        if app.config['TESTING'] is True:
            conn = pg.connect(dbname='fasttests', user='postgres',
                              password='0789')
        else:
            conn = pg.connect('postgres://dmyozauakukgim:78c6acc65cef8bc118a1e044dd422393a21a1018ee9cabbcd9769b4451ae6032@ec2-54-225-68-133.compute-1.amazonaws.com:5432/d88tp0iv0aqbgc', sslmode='require')
        self.conn = conn
        self.conn.autocommit = True
        self.cur = conn.cursor()

    def run(self, sql, data=None, command=None):
        info = None
        try:
            for query in sql:
                self.cur.execute(query, data)
                if command == 'SELECT':
                    info = self.cur.fetchall()
                elif command == 'UPDATE':
                    info = self.cur.rowcount
                else:
                    pass
            self.cur.close()
        except (Exception, pg.DatabaseError) as error:
            return error
        finally:
            if self.conn is not None:
                self.conn.close()
        return info

    def create_tables(self):
        sql_main = (
            """CREATE TABLE IF NOT EXISTS menu
                (
                food_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                price INTEGER NOT NULL,
                status VARCHAR(255) NOT NULL,
                tags VARCHAR(255) )""",
            """CREATE TABLE IF NOT EXISTS users
              (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                tel INTEGER NOT NULL,
                email VARCHAR(255),
                location VARCHAR(255) NOT NULL,
                key_point VARCHAR(255),
                role VARCHAR(20)
            )""",
            """CREATE TABLE IF NOT EXISTS orders
             (
                order_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                food_id INTEGER NOT NULL,
                name VARCHAR(255) NOT NULL,
                quantity INTEGER NOT NULL,
                comment VARCHAR(255),
                location VARCHAR(255) NOT NULL,
                amount INTEGER NOT NULL,
                status VARCHAR(255) NOT NULL,
                FOREIGN KEY (food_id) REFERENCES menu (food_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
             )""",
            """
               INSERT INTO Users(username, password, tel, email, location,
                                key_point,
                          role)
             VALUES('tanner','pass','0777','tom@dev.com','Bukoto','Andela',
                   'Admin') RETURNING user_id;
           """
        )
        
        response_1 = self.run(sql_main)
        print(response_1)

    def clean_tables(self):
        sql = ("DELETE FROM orders", "DELETE FROM users", "DELETE FROM menu")
        self.run(sql)
