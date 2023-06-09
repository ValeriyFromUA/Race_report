from pathlib import Path

from flasgger import Swagger
from flask import Flask
from flask_restful import Api

VER = 'v2'
APP = Flask(__name__)
API = Api(APP)
SWAGGER = Swagger(APP)
HOST = 'localhost'
PORT = 5000
DEBUG = False

START = 'start.log'
END = 'end.log'
ABBREVIATIONS = 'abbreviations.txt'

# static/db settings
DATA_FOLDER_IN_APP = 'static'
APP_FOLDER = Path(__file__).resolve().parent
PATH = Path(APP_FOLDER / DATA_FOLDER_IN_APP)
