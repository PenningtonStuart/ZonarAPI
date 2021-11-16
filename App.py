from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "Zonar"  # obviously not something that should be pushed to production
api = Api(app)

jwt = JWT(app, authenticate, identity)  # generates a new endpoint /auth

books = []


class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('author',
                        type=str,
                        required=True,
                        help="This is a required field"
                        )

    @jwt_required()
    def get(self, title):
        book = next(filter(lambda x: x['book'] == book, books),
                    None)  # using the lambda instead of and if iteration.... Can break program if there are no items in books
        return {'book': book}, 200 if book is not None else 404  # this line can be shortened

    def post(self, title):
        if next(filter(lambda x: x['book'] == book, books), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(title)}, 400

        data = Book.parser.parse_args()

        book = {'title': title, 'author': data[
            'author']}  # current bug when dealing with json and postman Some sort of mismatch bor json format interpretation
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


api.add_resource(Book, '/book/<string:title>')
api.add_resource(BooksList, '/books')

app.run(port=5000, debug=True)
