from flask import current_app

from app.auth import AuthHandler
from app.db import get_db
from app.helpers.exceptions import FailedException


class UserHandler:
    def __init__(self):
        self.db = get_db()

    def register_user(self, data):
        required_keys = {'username', 'password', 'name'}
        if not set(data.keys()).issubset(required_keys):
            return {'status_id': 0, 'reason': 'Incomplete Information!'}
        validated_user = self._validate_user(data)
        result = self.db.insert_doc(validated_user, current_app.config['MONGO_DBNAME'],
                                    current_app.config['MONGO_COL_USERS'])
        if result.inserted_id:
            return {'status_id': 1, 'message': 'User Registered Successfully!'}
        else:
            return {'status_id': 0, 'message': 'Cannot Register User!'}

    def _validate_user(self, user, login=False):
        validated_data = dict()
        validated_data['username'] = user['username'].strip()
        if user.get('name'):
            validated_data['name'] = user['name'].strip()
        if self.db.filter_one_doc(current_app.config['MONGO_DBNAME'], current_app.config['MONGO_COL_USERS'],
                                  {'username': validated_data['username']}) and not login:
            raise FailedException('Username already exists!')
        hash_data = {"username": validated_data['username'], "password": user['password'].strip()}
        validated_data['hash'] = AuthHandler.encrypt_data(hash_data)
        return validated_data

    def login(self, data):
        required_keys = {'username', 'password'}
        if not set(data.keys()).issubset(required_keys):
            return {'status_id': 0, 'reason': 'Incomplete Information!'}
        validated_user = self._validate_user(data, login=True)
        user = self.db.filter_one_doc(current_app.config['MONGO_DBNAME'], current_app.config['MONGO_COL_USERS'],
                                      validated_user)
        if user:
            user.pop('hash')
            return {'status_id': 1, 'token': validated_user["hash"], 'user': user}
        else:
            return {'status_id': 0, 'reason': 'Username or Password is wrong'}
