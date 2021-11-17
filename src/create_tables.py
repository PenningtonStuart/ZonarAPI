import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, first_name text, last_name text, email text, " \
               "password text) "
cursor.execute(create_table)

connection.commit()

connection.close()
