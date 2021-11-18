from flask_restful import Resource, reqparse
#from flask_jwt import jwt_required
import sqlite3

from flask import request

class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str,
                        required=False,
                        help="Title is a required field"
                        )
    parser.add_argument('author',
                        type=str,
                        required=True,
                        help="Author is a required field"
                        )
    parser.add_argument('isbn',
                        type=str,
                        required=True,
                        help="ISBN is a required field"
                        )
    parser.add_argument('pub_date',
                        type=str,
                        required=True,
                        help="Publication Date is a required field"
                        )

    @classmethod
    def find_by_title(cls, title):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM book WHERE title=?"
        result = cursor.execute(query, (title,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'book': {'title': row[0], 'author': row[1], 'isbn': row[2], 'pub_date': row[3]}}, 200
        else:
            return {'Message': "Item not found"}, 404

    @classmethod
    def insert(cls, book):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO book VALUES (?, ?, ?, ?)"
        cursor.execute(query, (book['title'], book['author'], book['isbn'], book['pub_date']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, book):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE book SET author=?, isbn=?, pub_date=? WHERE title=?"
        cursor.execute(query, (book['author'], book['isbn'], book['pub_date'], book['title']))

        connection.commit()
        connection.close()

    #@jwt_required()
    def get(self, title):
        book = self.find_by_title(title)
        return book

    def post(self, title):
        print(request.json)
        print(request.data)
        print(request.values)
        if self.find_by_title(title)[1]==200:
            return {'message': "An item with name '{}' already exists.".format(title)}, 409
        print("hi")
        data = Book.parser.parse_args()
        print("Hello")
        book = {'title': title, 'author': data['author'], 'isbn': data['isbn'], 'pub_date': data['pub_date']}
        print(book)

        self.insert(book)

        return book, 201

    def put(self, title):
        data = Book.parser.parse_args()

        book = self.find_by_title(title)
        updated_book = {'title': title, 'author': data['author'], 'isbn': data['isbn'], 'pub_date': data['pub_date']}

        if book is None:
            self.insert(updated_book)
        else:
            self.update(updated_book)
        return updated_book, 200

    def delete(self, title):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM book WHERE title=?"
        cursor.execute(query, (title))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}, 200


class BooksList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM book"
        result = cursor.execute(query)
        books = []
        for row in result:
            books.append({'title': row[0], 'author': row[1], 'isbn': row[2], 'pub_date': row[3]})

        connection.close()

        return {'books': books}
