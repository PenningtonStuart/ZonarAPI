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

    @classmethod
    def find_by_title(cls, title):
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
        cursor.execute(query, ( book['author'], book['isbn'], book['pub_date'], book['title']))

        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, title):
        book = self.find_by_title(title)
        if book:
            return book
        return {'Message': "Item not found"}, 404

    def post(self, title):
        if self.find_by_title(title):
            return {'message': "An item with name '{}' already exists.".format(title)}, 400

        data = Book.parser.parse_args()
        book = {'title': title, 'author': data['author'], 'isbn': data['isbn'], 'pub_date': data['pub_date']}

        try:
            self.insert(title)
        except:
            return {"message": "An error occurred while attempting to insert an item"}, 500

        return book, 201

    def put(self, title):
        data = Book.parser.parse_args()

        book = self.find_by_title(title)
        updated_book = {'title': title, 'author': data['author'], 'isbn': data['isbn'], 'pub_date': data['pub_date']}

        if book is None:
            try:
                self.insert(updated_book)
            except:
                return {"message": "An error occurred while trying to insert the book"}, 500
        else:
            try:
                self.update(updated_book)
            except:
                return {"message": "An error occurred while trying to update the book"}, 500

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
        return {'books': books}
