from flask_restful import Resource, reqparse
from models.odooURL import OdooURLModel


class OdooURL(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url',
                        type=str,
                        required=True,
                        help="need an url"
                        )
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="need odoo username"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="need odoo password"
                        )

    parser2 = reqparse.RequestParser()
    parser2.add_argument('url',
                        type=str,
                        required=True,
                        help="need an url"
                        )


    #@jwt_required()
    def get(self):
        data = OdooURL.parser2.parse_args()
        url = data["url"]
        odooURL = OdooURLModel.find_by_url(url)
        if odooURL:
            return odooURL.json()
        return {'message': 'url not found'}, 404

    def post(self):
        
        data = OdooURL.parser.parse_args()
        url = data["url"]

        if OdooURLModel.find_by_url(url):
            return {'message': "The url '{}' already exists.".format(url)}, 400

        odooURL = OdooURLModel(**data)

        try:
            odooURL.save_to_db()
        except:
            return {"message": "An error occurred inserting the url"}, 500

        return odooURL.json(), 201

    # def delete(self, name):
    #     odooURL = OdooURLModel.find_by_url(url)
    #     if odooURL:
    #         odooURL.delete_from_db()
    #         return {'message': 'Item deleted.'}
    #     return {'message': 'Item not found.'}, 404

    # def put(self, name):
    #     data = OdooURL.parser.parse_args()

    #     odooURL = OdooURLModel.find_by_name(name)

    #     if odooURL:
    #         odooURL.price = data['price']
    #     else:
    #         odooURL = OdooURLModel(name, **data)

    #     odooURL.save_to_db()

    #     return item.json()


class OdooURLList(Resource):
    def get(self):
        return {'odooURLs': list(map(lambda x: x.json(), OdooURLModel.query.all()))}
