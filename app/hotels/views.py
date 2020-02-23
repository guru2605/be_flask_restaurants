from flask import Blueprint, jsonify, request
from .handler import HotelsHandler


hotels = Blueprint('hotels', __name__)


@hotels.route('', methods=["POST"])
def get_all_hotels():
    return jsonify(HotelsHandler().get_all_hotels(request.json))


@hotels.route('/get_regions', methods=["GET"])
def get_all_regions():
    return jsonify(HotelsHandler().get_all_regions())

