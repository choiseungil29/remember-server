import os

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.environ['SECRET_KEY']

from app.api import blueprint_api

app.register_blueprint(blueprint_api)