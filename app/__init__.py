from flask import Flask

app = Flask(__name__)


from app.api import blueprint_api

app.register_blueprint(blueprint_api)