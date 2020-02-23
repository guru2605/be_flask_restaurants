import jwt
from flask import current_app


class AuthHandler:
    @staticmethod
    def decrypt_data(data):
        """
        This method decrypts data
        :param data:
        :return:
        """
        return jwt.decode(data, current_app.config['SECRET'], algorithm='HS256')

    @staticmethod
    def encrypt_data(data):
        """
        This method encrypts data
        :param data:
        :return:
        """
        return jwt.encode(data, current_app.config['SECRET'], algorithm='HS256').decode('utf-8')
