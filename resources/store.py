from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        try:
            store = StoreModel.findByName(name)
        except:
            return {'message': 'Error while searching for the store'}, 500
        
        if store:
            return {'store': store.json()}, 200        
        return {'message': 'store not found'}, 404

    def post(self, name):
        if StoreModel.findByName(name):
            return {'message': 'This store already exists. Don´t create again'}, 400
        store = StoreModel(name)
        
        try:
            store.saveToDb()
        except:
            return {"message": "Error while inserting the store"}, 500

        return store.json(), 201

    
    def delete(self, name):
        store = StoreModel.findByName(name)
        if store:
            store.deleteFromDb()
            return {'message': 'Store deleted successfully :)'}, 200
        else:
            return {'message': 'Store not found in database :/'}, 400

class StoreList(Resource):
    def get(self):
        stores = StoreModel.query.all()

        if not stores:
            return {'message': 'No stores registered in the database :/'}, 400

        return {'stores': [store.json() for store in stores]},200