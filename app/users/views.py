from flask import Blueprint, jsonify, request
from .handler import UserHandler


users = Blueprint('users', __name__)


@users.route('/register', methods=['POST'])
def register_user():
    return jsonify(UserHandler().register_user(request.json))


@users.route('/login', methods=['POST'])
def login():
    return jsonify(UserHandler().login(request.json))
