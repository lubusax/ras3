from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class odooURI(Resource):
    def get(self, _id):
        return {'odooURI': _id}

api.add_resource(odooURI, '/odooURI/<string:_id>')

app.run(port=5000)