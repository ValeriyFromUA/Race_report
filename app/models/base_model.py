from peewee import Model

from app.db_config import db


class BaseModel(Model):
    class Meta:
        database = db
