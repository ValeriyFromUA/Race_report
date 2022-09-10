import unittest
from peewee import SqliteDatabase
from app.models_report import ReportModel, ResultsModel
from functools import wraps
from app.report_DB import app

MODELS = (ReportModel, ResultsModel)


def use_test_db(method):
    @wraps(method)
    def inner(self):
        test_db = SqliteDatabase(':memory:')
        with test_db.bind_ctx(MODELS):
            test_db.create_tables(MODELS)
            try:
                method(self)
            finally:
                test_db.drop_tables(MODELS)

    return inner


class ReportDBTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    @use_test_db
    def test_report(self):
        # src.report.monaco (converting_data.py) sorted the report by lap time
        data = [
            {'abbr': 'SSW', 'name': 'Sergey Sirotkin', 'team': 'WILLIAMS MERCEDES', 'lap_time': '00:04:47.294000'},
            {'abbr': 'EOF', 'name': 'Esteban Ocon', 'team': 'FORCE INDIA MERCEDES', 'lap_time': '00:05:46.972000'},
            {'abbr': 'LHM', 'name': 'Lewis Hamilton', 'team': 'MERCEDES', 'lap_time': '00:06:47.540000'},
        ]
        fields = [ReportModel.abbr, ReportModel.name, ReportModel.team, ReportModel.lap_time]
        ReportModel.insert_many(data, fields).execute()
        response = self.client.get("/api/v2/report", query_string={"format": "json"})
        with self.subTest():
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers["Content-Type"], "application/json")
            self.assertEqual(response.json, [
                ['Sergey Sirotkin', 'WILLIAMS MERCEDES', '00:04:47.294000'],
                ['Esteban Ocon', 'FORCE INDIA MERCEDES', '00:05:46.972000'],
                ['Lewis Hamilton', 'MERCEDES', '00:06:47.540000'],
            ])

    @use_test_db
    def test_report_asc(self):
        # src.report.monaco (converting_data.py) sorted the report by lap time
        data = [
            {'abbr': 'SSW', 'name': 'Sergey Sirotkin', 'team': 'WILLIAMS MERCEDES', 'lap_time': '00:04:47.294000'},
            {'abbr': 'EOF', 'name': 'Esteban Ocon', 'team': 'FORCE INDIA MERCEDES', 'lap_time': '00:05:46.972000'},
            {'abbr': 'LHM', 'name': 'Lewis Hamilton', 'team': 'MERCEDES', 'lap_time': '00:06:47.540000'},
        ]
        fields = [ReportModel.abbr, ReportModel.name, ReportModel.team, ReportModel.lap_time]
        ReportModel.insert_many(data, fields).execute()
        response = self.client.get("/api/v2/report/order=asc", query_string={"format": "json"})
        with self.subTest():
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers["Content-Type"], "application/json")
            self.assertEqual(response.json, [
                ['Sergey Sirotkin', 'WILLIAMS MERCEDES', '00:04:47.294000'],
                ['Esteban Ocon', 'FORCE INDIA MERCEDES', '00:05:46.972000'],
                ['Lewis Hamilton', 'MERCEDES', '00:06:47.540000'], ])

    @use_test_db
    def test_report_desc(self):
        # src.report.monaco (converting_data.py) sorted the report by lap time
        data = [
            {'abbr': 'SSW', 'name': 'Sergey Sirotkin', 'team': 'WILLIAMS MERCEDES', 'lap_time': '00:04:47.294000'},
            {'abbr': 'EOF', 'name': 'Esteban Ocon', 'team': 'FORCE INDIA MERCEDES', 'lap_time': '00:05:46.972000'},
            {'abbr': 'LHM', 'name': 'Lewis Hamilton', 'team': 'MERCEDES', 'lap_time': '00:06:47.540000'},
        ]
        fields = [ReportModel.abbr, ReportModel.name, ReportModel.team, ReportModel.lap_time]
        ReportModel.insert_many(data, fields).execute()
        response = self.client.get("/api/v2/report/order=desc", query_string={"format": "json"})
        with self.subTest():
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers["Content-Type"], "application/json")
            self.assertEqual(response.json, [
                ['Lewis Hamilton', 'MERCEDES', '00:06:47.540000'],
                ['Esteban Ocon', 'FORCE INDIA MERCEDES', '00:05:46.972000'],
                ['Sergey Sirotkin', 'WILLIAMS MERCEDES', '00:04:47.294000'],
            ])

    @use_test_db
    def test_report_one_driver(self):
        # src.report.monaco (converting_data.py) sorted the report by lap time
        data = [
            {'abbr': 'SSW', 'name': 'Sergey Sirotkin', 'team': 'WILLIAMS MERCEDES', 'lap_time': '00:04:47.294000'},
            {'abbr': 'EOF', 'name': 'Esteban Ocon', 'team': 'FORCE INDIA MERCEDES', 'lap_time': '00:05:46.972000'},
            {'abbr': 'LHM', 'name': 'Lewis Hamilton', 'team': 'MERCEDES', 'lap_time': '00:06:47.540000'},
        ]
        fields = [ReportModel.abbr, ReportModel.name, ReportModel.team, ReportModel.lap_time]
        ReportModel.insert_many(data, fields).execute()
        response = self.client.get("/api/v2/report/order=asc/driver=Esteban Ocon", query_string={"format": "json"})
        with self.subTest():
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers["Content-Type"], "application/json")
            self.assertEqual(response.json, ['Esteban Ocon', 'FORCE INDIA MERCEDES', '00:05:46.972000'])


if __name__ == '__main__':
    unittest.main()
