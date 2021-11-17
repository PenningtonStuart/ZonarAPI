from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str,
                        required=True,
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

    @jwt_required()
    def get(self, title):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM book WHERE title=?"
        result = cursor.execute(query, (title,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'book': {'title': row[0], 'author': row[1], 'isbn': row[2], 'pub_date': row[3]}}
        else:
            return {'Message': "Item not found"}, 404

    def post(self, title):
        if next(filter(lambda x: x['book'] == book, books), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(title)}, 400

        data = Book.parser.parse_args()

        book = {'title': title, 'author': data['author']}  # current bug when dealing with json and postman Some sort of mismatch bor json format interpretation
        books.append(book)
        return book, 201

    def delete(self, title):
        global books
        books = list(filter(lambda x: x['title'] != title, books))
        return {'message': 'Item deleted'}, 200

    def put(self, title):
        data = Book.parser.parse_args()

        book = next(filter(lambda x: x['book'] == book, books), None)
        if book is None:
            book = {'title': title, 'author': data['author']}
            books.append(book)
        else:
            book.update(data)
        return book, 200


class BooksList(Resource):
    def get(self):
        return {'books': books}

