import json
from typing import List, TypedDict

from flask import Response
from src.report.monaco import build_report, get_abbr_and_time_data

from flask_app.db_config import db
from flask_app.models import ReportModel, ResultsModel
from flask_app.settings import END, PATH, START


class StartEndData(TypedDict):
    abbr: str
    start_time: str
    end_time: str


class Driver(TypedDict):
    driver: str
    team: str
    lap_time: str


def preparing_start_end_data() -> List[dict]:
    """Getting start/end time static, preparing to insert into database"""
    start_end = {}
    start_end_list: List[StartEndData] = []
    for key in get_abbr_and_time_data(PATH, START):
        if key in get_abbr_and_time_data(PATH, END):
            start_end = {
                'abbr': key,
                'start_time': get_abbr_and_time_data(PATH, START)[key],
                'end_time': get_abbr_and_time_data(PATH, END)[key],
            }
        start_end_list.append(start_end)
    return start_end_list


def create_db_report():
    """Creating DB and Adding static"""
    with db:
        db.create_tables([ReportModel])
        ReportModel.insert_many(build_report(PATH)[1]).execute()
    with db:
        db.create_tables([ResultsModel])
        ResultsModel.insert_many(preparing_start_end_data()).execute()


def create_report_from_db() -> List[dict]:
    """Converting db file to list"""
    report_list = []
    query = ReportModel.select()
    for driver in query:
        data = {
            'driver': driver.name,
            'team': driver.team,
            'lap_time': str(driver.lap_time)
        }
        report_list.append(data)
    return report_list


def create_drivers_from_db() -> List[dict]:
    """Converting db file to list"""
    drivers_list = []
    query = ReportModel.select()
    for driver in query:
        drivers = {
            'abbr': driver.abbr,
            'diver': driver.name
        }
        drivers_list.append(drivers)
    return drivers_list


def create_one_drivers_from_db(abbr):
    query = ReportModel.select()
    for driver in query:
        if abbr.upper() == driver.abbr:
            data: Driver = {
                'driver': driver.name,
                'team': driver.team,
                'lap_time': str(driver.lap_time)
            }
            return json.dumps(data)
    return Response("Driver not found, please check abbreviation", status=404)
