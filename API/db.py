import psycopg2 as pg


class Database:

    def __init__(self, app):
        if app.config['TESTING'] is True:
            conn = pg.connect(dbname='fasttests', user='postgres',
                              password='0789')
        else:
            conn = pg.connect(dbname='fastfood', user='postgres',
                              password='0789')
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
            """CREATE DATABASE fastfood 
            """,
            """"CREATE TABLE menu IF NOT EXISTS
                (
                food_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                price INTEGER NOT NULL,
                status VARCHAR(255) NOT NULL,
                tags VARCHAR(255) )""",
            """CREATE TABLE users IF NOT EXISTS
              (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                tel INTEGER NOT NULL,
                email VARCHAR(255),
                location VARCHAR(255) NOT NULL,
                key_point VARCHAR(255),
                role VARCHAR(20),
            )""",
            """CREATE TABLE orders IF NOT EXISTS
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
             )"""
        )
        sql_tests = (
            """CREATE DATABASE fasttests
               IF NOT EXISTS
            """,
            """"CREATE TABLE menu IF NOT EXISTS
                (
                food_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                price INTEGER NOT NULL,
                status VARCHAR(255) NOT NULL,
                tags VARCHAR(255) )""",
            """CREATE TABLE users IF NOT EXISTS
              (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                tel INTEGER NOT NULL,
                email VARCHAR(255),
                location VARCHAR(255) NOT NULL,
                key_point VARCHAR(255),
                role VARCHAR(20),
            )""",
            """CREATE TABLE orders IF NOT EXISTS
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
             )"""
        )

        response_2 = self.run(sql_tests)
        return response_2

    def clean_tables(self):
        sql = ("DELETE FROM orders", "DELETE FROM users", "DELETE FROM menu")
        self.run(sql)
