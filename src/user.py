import sqlite3


class User:
    def __init__(self, _id, first_name, last_name, email, password):
        self.id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    @classmethod
    def find_by_username(cls, email):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM user WHERE email=?"
        result = cursor.execute(query, (email,))
        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2], row[3], row[4])
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM user WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2], row[3], row[4])
        else:
            user = None

        connection.close()
        return user
