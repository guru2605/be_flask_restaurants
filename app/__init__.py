import os
from datetime import datetime

from bson import ObjectId
from flask import Flask
from flask.json import JSONEncoder
from flask_cors import CORS
from pymongo.command_cursor import CommandCursor
from app.helpers.exceptions import FailedException


class CustomJSONEncoder(JSONEncoder):
    """
    Class consist action related to Custom JSON Encoding
    """
    def default(self, obj):
        """
        Method consist of operations performed to encode different data-types into JSON format
        :param obj:
        :return:
        """
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return str(obj)
        if isinstance(obj, CommandCursor):
            return list(obj)
        return JSONEncoder.default(self, obj)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='development',
    )
    app.config.from_pyfile('config.py', silent=True)
    app.json_encoder = CustomJSONEncoder
    CORS(app)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from app.hotels.views import hotels
    app.register_blueprint(hotels, url_prefix='/hotels')

    from app.users.views import users
    app.register_blueprint(users)

    app.register_error_handler(FailedException, FailedException().handle_failed_exception)

    return app
