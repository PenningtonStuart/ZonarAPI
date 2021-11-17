import sqlite3
from flask_restful import Resource, reqparse


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


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        help="first name cannot be empty."
                        )
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help="last name cannot be empty."
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="email cannot be empty."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password cannot be empty."
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['email']):  # prevents duplicate entries in the DB
            return {"message": "A user with that username already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO user VALUES (NULL, ?, ?, ?, ?)"
        cursor.execute(query, (data['first_name'], data['last_name'], data['email'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User Created"}, 201
