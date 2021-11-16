from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
app.secret_key = "Zonar" #obviously not something that should be pushed to production
api = Api(app)

books = []
class Book(Resource):
    def get(self, title):
        book = next(filter(lambda x: x['book'] == book, books), None) #using the lambda instead of and if iteration.... Can break program if there are no items in books
        return {'book': book}, 200 if book is not None else 404 #this line can be shortened

    def post(self, title):
        if next(filter(lambda x: x['book'] == book, books), None) is not None:
            return{'message': "An item with name '{}' already exists.".format(title)}, 400
        data = request.get_json()
        book = {'title': title, 'author': data['author']} #current bug when dealing with json and postman Some sort of mismatch bor json format interpretation
        books.append(book)
        return book, 201

class BooksList(Resource):
    def get(self):
        return {'books': books}

api.add_resource(Book, '/book/<string:title>')
api.add_resource(BooksList, '/books')

app.run(port=5000, debug=True)