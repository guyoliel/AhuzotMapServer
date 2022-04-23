import os
from flask import Flask, Blueprint
from dotenv import load_dotenv
from flask_cors import CORS
from parking_lots_controller import parking_lots_controller

app = Flask(__name__)
api = Blueprint('api','api',url_prefix='/api')
api.register_blueprint(parking_lots_controller)
app.register_blueprint(api)

CORS(app)

if __name__ == "__main__":
    load_dotenv()
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.run(host="127.0.0.1", port=port)
