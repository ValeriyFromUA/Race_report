from unittest import TestCase
from unittest.mock import patch

from flask_app.db_managers import (get_drivers_from_db, get_one_driver_from_db, get_report_from_db,
                                   preparing_start_end_data)
from flask_app.models import ReportModel
from tests import MODELS, test_db


class TestDBManagers(TestCase):

    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        data = [
            {'abbr': 'XXX', 'name': 'Sergey Sirotkin', 'team': 'WILLIAMS MERCEDES', 'lap_time': '00:04:47.294000'},
            {'abbr': 'YYY', 'name': 'Esteban Ocon', 'team': 'FORCE INDIA MERCEDES', 'lap_time': '00:05:46.972000'},
            {'abbr': 'ZZZ', 'name': 'Lewis Hamilton', 'team': 'MERCEDES', 'lap_time': '00:06:47.540000'},
        ]
        fields = [ReportModel.abbr, ReportModel.name, ReportModel.team, ReportModel.lap_time]
        ReportModel.insert_many(data, fields).execute()

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    @patch('flask_app.db_managers.get_abbr_and_time_data')
    def test_preparing_start_end_data(self, mock_func):
        mock_func.return_value = {'OOO': '12:02:58.917', 'III': '13:02:58.917', 'EEE': '14:02:58.917'}
        result = preparing_start_end_data()
        self.assertEqual(result, [{'abbr': 'OOO', 'start_time': '12:02:58.917', 'end_time': '12:02:58.917'},
                                  {'abbr': 'III', 'start_time': '13:02:58.917', 'end_time': '13:02:58.917'},
                                  {'abbr': 'EEE', 'start_time': '14:02:58.917', 'end_time': '14:02:58.917'}])

    def test_get_report_from_db(self):
        self.assertEqual(get_report_from_db(),
                         [{'driver': 'Sergey Sirotkin', 'lap_time': '00:04:47.294000', 'team': 'WILLIAMS MERCEDES'},
                          {'driver': 'Esteban Ocon', 'lap_time': '00:05:46.972000', 'team': 'FORCE INDIA MERCEDES'},
                          {'driver': 'Lewis Hamilton', 'lap_time': '00:06:47.540000', 'team': 'MERCEDES'}])

    def test_get_drivers_from_db(self):
        self.assertEqual(get_drivers_from_db(),
                         [{'abbr': 'XXX', 'driver': 'Sergey Sirotkin'},
                          {'abbr': 'YYY', 'driver': 'Esteban Ocon'},
                          {'abbr': 'ZZZ', 'driver': 'Lewis Hamilton'}])

    def test_get_one_driver_from_db(self):
        self.assertEqual(get_one_driver_from_db('yyy'),
                         {'driver': 'Esteban Ocon', 'lap_time': '00:05:46.972000', 'team': 'FORCE INDIA MERCEDES'})

    def test_get_one_driver_from_db_bad(self):
        self.assertEqual(get_one_driver_from_db('xyz'), None)
