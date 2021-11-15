from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

books = []
class Book(Resource):
    def get(self, title):
        for book in books:
            if book['title'] == title:
                return book
        return {'book': None}, 404

    def post(self, title):
        book = {'title': 'Treasure Island', 'author': 'Jules Vern'}
        books.append(book)
        return book, 201

class BooksList(Resource):
    def get(self):
        return {'books': books}

api.add_resource(Book, '/book/<string:title>')
api.add_resource(BooksList, '/books')

app.run(port=5000, debug=True)