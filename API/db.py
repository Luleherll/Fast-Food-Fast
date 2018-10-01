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
                else:
                    pass
            self.cur.close()
        except (Exception, pg.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return info

    def drop(self):
        sql = ("DELETE FROM orders", "DELETE FROM users", "DELETE FROM menu")
        self.run(sql)
