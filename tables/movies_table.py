from dbconnection import *

class MoviesTable:
    dbconn = None

    def table_name(self):
        return self.dbconn.prefix + "movies"

    def create(self):
        cur = self.dbconn.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            title VARCHAR(255) PRIMARY KEY,
            genre VARCHAR(100) NOT NULL,
            duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
            minimum_age INTEGER NOT NULL CHECK (minimum_age >= 0),
            country_name VARCHAR(100) REFERENCES countries(country_name) ON DELETE SET NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.dbconn.conn.commit()

    def all(self, limit=None, offset=None):
        sql = "SELECT title, genre, duration_minutes, minimum_age, country_name FROM " + self.table_name() + " ORDER BY title"
        if limit:
            sql += f" LIMIT {limit} OFFSET {offset}"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def insert_one(self, title, genre, duration, age, country):
        cur = self.dbconn.conn.cursor()
        cur.execute(
            "INSERT INTO movies(title, genre, duration_minutes, minimum_age, country_name) VALUES (%s, %s, %s, %s, %s)",
            (title, genre, duration, age, country)
        )
        self.dbconn.conn.commit()

