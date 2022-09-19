from typing import List, TypedDict

from src.report.monaco import build_report, get_abbr_and_time_data

from app.db_config import db
from app.models.report_model import ReportModel
from app.models.results_model import ResultsModel
from app.settings import *


class StartEndData(TypedDict):
    abbr: str
    start_time: str
    end_time: str


def preparing_start_end_data():
    """getting start/end time static, preparing to insert into database"""

    start_end = {}
    start_end_list: List[StartEndData] = []
    for key in get_abbr_and_time_data(path, START):
        if key in get_abbr_and_time_data(path, END):
            start_end = {
                'abbr': key,
                'start_time': get_abbr_and_time_data(path, START)[key],
                'end_time': get_abbr_and_time_data(path, END)[key],
            }
        start_end_list.append(start_end)
    return start_end_list


def create_db_report():
    """Creating DB and Adding static"""
    data = build_report(path)[1]
    with db:
        db.create_tables([ReportModel])
        ReportModel.insert_many(data).execute()
    with db:
        db.create_tables([ResultsModel])
        ResultsModel.insert_many(preparing_start_end_data()).execute()


def create_report_from_db() -> List[tuple]:
    """converting db file to list"""
    data_list = []
    query = ReportModel.select()
    for driver in query:
        data_string = (driver.name, driver.team, str(driver.lap_time))
        data_list.append(data_string)
    return data_list
