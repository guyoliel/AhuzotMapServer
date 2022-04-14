from bson import json_util
from flask import Flask, request
import ahuzot_helper as ah
from parkings_db_helper import ParkingsDbHelper

app = Flask(__name__)


@app.route("/api/get_all_lots")
def get_all_lots():
    db_helper = ParkingsDbHelper('localhost', 27017)
    return json_util.dumps(db_helper.get_all_lots())


@app.route("/api/get_nearby_lots", methods=['POST'])
def get_near_lots():
    body = request.json
    db_helper = ParkingsDbHelper('localhost', 27017)
    return json_util.dumps(db_helper.get_near_lots(body['point'], body['distance']))


@app.route("/api/upsert_lots", methods=['POST'])
def upsert_lots():
    lot_urls = ah.getAvailableParkingLots()
    lot_results = ah.getAllLotsStatus(lot_urls)
    db_helper = ParkingsDbHelper('localhost', 27017)
    db_helper.upsert_parking_lots(lot_results)
    return 'ok'
