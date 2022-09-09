from peewee import SqliteDatabase, Model, PrimaryKeyField, TextField, TimeField, ForeignKeyField

db = SqliteDatabase('data/report_monaco_database.db')


class BaseModel(Model):
    class Meta:
        database = db


class ReportModel(BaseModel):
    id = PrimaryKeyField(unique=True)
    abbr = TextField()
    name = TextField()
    team = TextField()
    lap_time = TimeField()

    class Meta:
        order_by = 'lap_time'
        db_table = 'reports'


class ResultsModel(BaseModel):
    abbr = ForeignKeyField(model=ReportModel, field='abbr', backref='results', unique=True)
    start_time = TextField()
    end_time = TextField()

    class Meta:
        order_by = 'abbr'
        db_table = 'results'
