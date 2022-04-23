from flask import Blueprint, request
import ahuzot_helper as ah
from parkings_db_helper import ParkingsDbHelper
from bson import json_util
import os

parking_lots_controller = Blueprint(
    'parking_lots', __name__, url_prefix='/parking_lots')


@parking_lots_controller.route("/get_all_lots")
def get_all_lots():
    db_helper = _get_db_helper()
    return json_util.dumps(db_helper.get_all_lots())


@parking_lots_controller.route("/get_nearby_lots", methods=['POST'])
def get_near_lots():
    body = request.json
    db_helper = _get_db_helper()
    return json_util.dumps(db_helper.get_near_lots(body['point'], body['distance']))


@parking_lots_controller.route("/upsert_lots", methods=['POST'])
def upsert_lots():
    lot_urls = ah.getAvailableParkingLots()
    lot_results = ah.getAllLotsStatus(lot_urls)
    db_helper = _get_db_helper()
    db_helper.upsert_parking_lots(lot_results)
    return 'ok'


def _get_db_helper():
    host = os.environ.get("MONGO_HOST", 'localhost')
    port = int(os.environ.get("MONGO_PORT", 27017))
    return ParkingsDbHelper(host, port)
