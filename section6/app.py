from flask import Flask
from flask_restful import Api
# from flask_jwt import JWT

# from security import authenticate, identity
# from resources.user import UserRegister
# from resources.item import Item, ItemList
# from resources.store import Store, StoreList
from resources.odooURL import OdooURL, OdooURLList


from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'secretsecret'

api = Api(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()


#jwt = JWT(app, authenticate, identity)  # /auth

# api.add_resource(Store, '/store/<string:name>')
# api.add_resource(StoreList, '/stores')
api.add_resource(OdooURL, '/odooURL')
api.add_resource(OdooURLList, '/odooURLs')
# api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
