from unittest import TestCase
from unittest.mock import patch

from flask_app.db_managers import (get_drivers_from_db, get_one_driver_from_db, get_report_from_db,
                                   preparing_start_end_data)
from flask_app.models import ReportModel
from tests import MODELS, test_db


class TestDBManagers(TestCase):
    get_report_list = []
    get_drivers_list = []
    data = [
        {'abbr': 'XXX', 'name': 'Sergey Sirotkin', 'team': 'WILLIAMS MERCEDES', 'lap_time': '00:04:47.294000'},
        {'abbr': 'YYY', 'name': 'Esteban Ocon', 'team': 'FORCE INDIA MERCEDES', 'lap_time': '00:05:46.972000'},
        {'abbr': 'ZZZ', 'name': 'Lewis Hamilton', 'team': 'MERCEDES', 'lap_time': '00:06:47.540000'},
    ]
    for el in data:
        report_data = {
            'driver': el['name'],
            'lap_time': el['lap_time'],
            'team': el['team']
        }
        get_report_list.append(report_data)
        drivers = {
            'abbr': el['abbr'],
            'driver': el['name']
        }
        get_drivers_list.append(drivers)

    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

        fields = [ReportModel.abbr, ReportModel.name, ReportModel.team, ReportModel.lap_time]
        ReportModel.insert_many(self.data, fields).execute()

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    @patch('flask_app.db_managers.get_abbr_and_time_data')
    def test_preparing_start_end_data(self, mock_func):
        abbr_O = 'OOO'
        time_O = '12:02:58.917'
        abbr_I = 'III'
        time_I = '13:02:58.917'
        abbr_E = 'EEE'
        time_E = '14:02:58.917'
        mock_func.return_value = {abbr_O: time_O, abbr_I: time_I, abbr_E: time_E}
        result = preparing_start_end_data()
        self.assertEqual(result, [{'abbr': abbr_O, 'start_time': time_O, 'end_time': time_O},
                                  {'abbr': abbr_I, 'start_time': time_I, 'end_time': time_I},
                                  {'abbr': abbr_E, 'start_time': time_E, 'end_time': time_E}])

    def test_get_report_from_db(self):
        self.assertEqual(get_report_from_db(), self.get_report_list)

    def test_get_drivers_from_db(self):
        self.assertEqual(get_drivers_from_db(), self.get_drivers_list)

    def test_get_one_driver_from_db(self):
        self.assertEqual(get_one_driver_from_db('yyy'),
                         {'driver': 'Esteban Ocon', 'lap_time': '00:05:46.972000', 'team': 'FORCE INDIA MERCEDES'})

    def test_get_one_driver_from_db_bad(self):
        self.assertEqual(get_one_driver_from_db('xyz'), None)
