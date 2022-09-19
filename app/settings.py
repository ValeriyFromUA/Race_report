from pathlib import Path

from flasgger import Swagger
from flask import Flask
from flask_restful import Api

VER = 'v2'
app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

START = 'start.log'
END = 'end.log'
ABBREVIATIONS = 'abbreviations.txt'

# static/db settings
DATA_FOLDER_IN_APP = 'static'
APP_FOLDER = Path(__file__).resolve().parent
path = Path(APP_FOLDER / DATA_FOLDER_IN_APP)
