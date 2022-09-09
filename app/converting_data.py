from src.report.monaco import build_report, get_abbr_and_time_data
from pathlib import Path
from app.models_report import ReportModel, db, ResultsModel

START = 'start.log'
END = 'end.log'
ABBREVIATIONS = 'abbreviations.txt'

# data/db settings
DATA_FOLDER_IN_APP = 'data'
APP_FOLDER = Path(__file__).resolve().parent
path = Path(APP_FOLDER / DATA_FOLDER_IN_APP)
data = build_report(path)[1]


# getting start/end time data, preparing to insert into database
def preparing_start_end_data():
    start_end = {}
    start_end_list = []
    for key in get_abbr_and_time_data(path, START):
        if key in get_abbr_and_time_data(path, END):
            start_end = {
                'abbr': key,
                'start_time': get_abbr_and_time_data(path, START)[key],
                'end_time': get_abbr_and_time_data(path, END)[key],
            }
        start_end_list.append(start_end)
    return start_end_list


# Creating DB and Adding data
def create_db_report():
    with db:
        db.create_tables([ReportModel])
        ReportModel.insert_many(data).execute()
    print('Done_report')
    with db:
        db.create_tables([ResultsModel])
        ResultsModel.insert_many(preparing_start_end_data()).execute()
    print('Done_results')


# converting db file to list
def create_report_from_db():
    data_list = []
    query = ReportModel.select()
    for driver in query:
        data_string = (driver.name, driver.team, str(driver.lap_time))
        data_list.append(data_string)
    return data_list
