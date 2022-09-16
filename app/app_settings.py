from flasgger import Swagger
from flask import Flask
from flask_restful import Api

VER = 'v2'
app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)
