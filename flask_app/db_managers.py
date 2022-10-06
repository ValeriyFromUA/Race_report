from typing import List, Optional, Dict

from src.report.monaco import build_report, get_abbr_and_time_data

from flask_app.db_config import db
from flask_app.models import ReportModel, ResultsModel
from flask_app.settings import END, PATH, START


def preparing_start_end_data() -> List[Dict]:
    """Getting start/end time static, preparing to insert into database"""
    start_time = get_abbr_and_time_data(PATH, START)
    end_time = get_abbr_and_time_data(PATH, END)
    start_end = {}
    start_end_list = []
    for key in start_time:
        if key in end_time:
            start_end = {
                'abbr': key,
                'start_time': start_time[key],
                'end_time': end_time[key],
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


def get_report_from_db() -> List[Dict]:
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


def get_drivers_from_db() -> List[Dict]:
    """Converting db file to list"""
    drivers_list = []
    query = ReportModel.select()
    for driver in query:
        drivers = {
            'abbr': driver.abbr,
            'driver': driver.name
        }
        drivers_list.append(drivers)
    return drivers_list


def get_one_driver_from_db(abbreviation: str) -> Optional[Dict]:
    """Checking for driver availability and returning data from the database"""
    driver = ReportModel.get_or_none(ReportModel.abbr == abbreviation.upper())
    if driver:
        data = {
            'driver': driver.name,
            'team': driver.team,
            'lap_time': str(driver.lap_time)
        }
        return data
