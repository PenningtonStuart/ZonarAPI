from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from book import Book, BooksList

app = Flask(__name__)
app.secret_key = "Zonar"  # obviously not something that should be pushed to production
api = Api(app)

jwt = JWT(app, authenticate, identity)  # generates a new endpoint /auth


api.add_resource(Book, '/book/<string:title>')
api.add_resource(BooksList, '/books')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)
