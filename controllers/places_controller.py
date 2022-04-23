from flask import Blueprint, request
from bson import json_util

places_controller = Blueprint(
    'places', __name__, url_prefix='/places')


@places_controller.route("/search_places")
def search_places():
    return 'ok'
