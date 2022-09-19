import os
from peewee import SqliteDatabase

db = SqliteDatabase(os.path.join(os.getcwd(), 'static\\report_monaco_database.db'))
