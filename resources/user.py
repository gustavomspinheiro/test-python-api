import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Username needs to be passed")
    parser.add_argument('password', type=str, required=True, help="Password needs to be passed")

    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.findByUsername(data['username'])
        
        if user:
            return {'message': 'User already exists =/'}, 400

        user = UserModel(**data)
        
        try:
            user.saveToDb()
            return {'message': f"User {user.username} created :)"}, 201

        except:
            return {'message': 'error while creating user in the database :/'}, 500

        
        