import os
from bson import json_util
from flask import Flask, request
import ahuzot_helper as ah
from parkings_db_helper import ParkingsDbHelper
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/get_all_lots")
def get_all_lots():
    db_helper = _get_db_helper()
    return json_util.dumps(db_helper.get_all_lots())


@app.route("/api/get_nearby_lots", methods=['POST'])
def get_near_lots():
    body = request.json
    db_helper = _get_db_helper()
    return json_util.dumps(db_helper.get_near_lots(body['point'], body['distance']))


@app.route("/api/upsert_lots", methods=['POST'])
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


if __name__ == "__main__":
    load_dotenv()
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.run(host="127.0.0.1", port=port)
