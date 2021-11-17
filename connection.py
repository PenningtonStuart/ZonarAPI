import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE user (id int, first_name text, last_name text, email text, password text)"
cursor.execute(create_table)

users = [
    (1, 'Katie', 'Pennington', 'katie.pennington@gmail.com', 'asdfg'),
    (2, 'Mike', 'Schwartz', 'mike.schwartz@gmail.com', 'qwerty'),
    (3, 'Ken', 'Holmes', 'ken.holmes@gmail.com', 'ghjkl')
]
insert_query = "INSERT INTO user VALUES(?, ?, ?, ?, ?)"
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM user"
for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()
