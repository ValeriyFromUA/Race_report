from peewee import ForeignKeyField, TextField

from .base_model import BaseModel
from .report_model import ReportModel


class ResultsModel(BaseModel):
    abbr = ForeignKeyField(model=ReportModel, field='abbr', backref='results', unique=True)
    start_time = TextField()
    end_time = TextField()

    class Meta:
        order_by = 'abbr'
