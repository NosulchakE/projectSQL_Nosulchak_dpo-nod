from dbconnection import *

class CountriesTable:
    dbconn = None

    def table_name(self):
        return self.dbconn.prefix + "countries"

    def create(self):
        cur = self.dbconn.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            country_name VARCHAR(100) PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.dbconn.conn.commit()

    def all(self, limit=None, offset=None):
        sql = "SELECT country_name FROM " + self.table_name() + " ORDER BY country_name"
        if limit:
            sql += f" LIMIT {limit} OFFSET {offset}"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def insert_one(self, name):
        cur = self.dbconn.conn.cursor()
        cur.execute("INSERT INTO countries(country_name) VALUES (%s)", (name,))
        self.dbconn.conn.commit()


