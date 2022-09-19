from peewee import PrimaryKeyField, TextField, TimeField
from .base_model import BaseModel


class ReportModel(BaseModel):
    id = PrimaryKeyField(unique=True)
    abbr = TextField()
    name = TextField()
    team = TextField()
    lap_time = TimeField()

    class Meta:
        order_by = 'lap_time'
        db_table = 'reports'
