from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="Price needs to be passed")
    parser.add_argument('store_id', type=float, required=True, help="Store id needs to be passed")


    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.findByName(name)
        except:
            return {'message': 'Error while searching for the item'}, 500
        
        if item:
            return item.json(), 200        
        return {'message': 'item not found'}, 404

    def post(self, name):
        if ItemModel.findByName(name):
            return {'message': 'This item already exists. Don´t create again'}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        
        try:
            item.saveToDb()
        except:
            return {"message": "Error while inserting the item"}, 500

        return item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.findByName(name)

        if item is None:
            try:
               item = ItemModel(name, data['price'],data['store_id'])
            except:
                return {'message': 'An error occurred creating the item'}, 500
        else:
            try:
                item.price = data['price']
            except:
                return {'message': 'An error occurred updating the item'}, 500
                
        item.saveToDb()
        return item.json()
              

    def delete(self, name):
        item = ItemModel.findByName(name)
        if item:
            item.deleteFromDb()
            return {'message': 'item deleted successfully :)'}, 200
        else:
            return {'message': 'item not found in database :/'}, 400

class ItemList(Resource):
    def get(self):
        items = ItemModel.query.all()

        if not items:
            return {'message': 'The items list is empty'}, 200
        
        return {'items': [item.json() for item in items]},200