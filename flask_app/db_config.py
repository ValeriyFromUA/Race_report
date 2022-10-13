import os

from peewee import SqliteDatabase

db = SqliteDatabase(os.path.join(os.getcwd(), 'flask_app/static/report_monaco_database.db'))
