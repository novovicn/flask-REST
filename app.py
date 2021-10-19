import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Items, Item
from resources.store import Store, StoreList
from db import db 


uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app = Flask(__name__)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = uri if uri else 'sqlite://data.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'
api = Api(app) 

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) #/auth

api.add_resource(Item, '/items/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(Store, '/stores/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)