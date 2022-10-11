from typing import List, Dict
from unittest import TestCase
from unittest.mock import patch

from flask_app.db_managers import (get_drivers_from_db, get_one_driver_from_db, get_report_from_db,
                                   preparing_start_end_data)
from flask_app.models import ReportModel
from tests import MODELS, test_db


class TestDBManagers(TestCase):
    data = [
        {'abbr': 'XXX', 'name': 'Sergey Sirotkin', 'team': 'WILLIAMS MERCEDES', 'lap_time': '00:04:47.294000'},
        {'abbr': 'YYY', 'name': 'Esteban Ocon', 'team': 'FORCE INDIA MERCEDES', 'lap_time': '00:05:46.972000'},
        {'abbr': 'ZZZ', 'name': 'Lewis Hamilton', 'team': 'MERCEDES', 'lap_time': '00:06:47.540000'},
    ]

    def get_report_list(self) -> List[Dict]:
        report_list = []
        for el in self.data:
            report_data = {
                'driver': el['name'],
                'lap_time': el['lap_time'],
                'team': el['team']
            }
            report_list.append(report_data)
        return report_list

    def get_drivers_list(self) -> List[Dict]:
        drivers_list = []
        for el in self.data:
            drivers = {
                'abbr': el['abbr'],
                'driver': el['name']
            }
            drivers_list.append(drivers)
        return drivers_list

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
        abbr_1, abbr_2, abbr_3 = 'OOO', 'III', 'EEE'
        time_1, time_2, time_3 = '12:02:58.917', '13:02:58.917', '14:02:58.917'
        mock_func.return_value = {abbr_1: time_1, abbr_2: time_2, abbr_3: time_3}
        result = preparing_start_end_data()
        self.assertEqual(result, [{'abbr': abbr_1, 'start_time': time_1, 'end_time': time_1},
                                  {'abbr': abbr_2, 'start_time': time_2, 'end_time': time_2},
                                  {'abbr': abbr_3, 'start_time': time_3, 'end_time': time_3}])

        self.assertEqual(mock_func.call_count, 2)

    def test_get_report_from_db(self):
        self.assertEqual(get_report_from_db(), self.get_report_list())

    def test_get_drivers_from_db(self):
        self.assertEqual(get_drivers_from_db(), self.get_drivers_list())

    def test_get_one_driver_from_db(self):
        self.assertEqual(get_one_driver_from_db('yyy'),
                         {'driver': 'Esteban Ocon', 'lap_time': '00:05:46.972000', 'team': 'FORCE INDIA MERCEDES'})

    def test_get_one_driver_from_db_bad(self):
        self.assertEqual(get_one_driver_from_db('xyz'), None)
