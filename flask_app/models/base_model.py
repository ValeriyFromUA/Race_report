from peewee import Model

from flask_app.db_config import db


class BaseModel(Model):
    class Meta:
        database = db
