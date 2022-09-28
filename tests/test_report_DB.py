import unittest

from flask_app.app import APP
from flask_app.models import ReportModel
from tests import MODELS, test_db


class ReportDBTest(unittest.TestCase):

    def setUp(self):
        APP.testing = True
        self.client = APP.test_client()

        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_report(self):
        """src.report.monaco (converting_data.py) sorted the report by lap time"""
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
            self.assertEqual(response.json, (
                '[{"driver": "Sergey Sirotkin", "team": "WILLIAMS MERCEDES", "lap_time": ''"00:04:47.294000"},'
                ' {"driver": "Esteban Ocon", "team": "FORCE INDIA ''MERCEDES", "lap_time": "00:05:46.972000"},'
                ' {"driver": "Lewis Hamilton", ''"team": "MERCEDES", "lap_time": "00:06:47.540000"}]'))

    def test_report_asc(self):
        """src.report.monaco (converting_data.py) sorted the report by lap time"""
        data = [
            {'abbr': 'SSW', 'name': 'Sergey Sirotkin', 'team': 'WILLIAMS MERCEDES', 'lap_time': '00:04:47.294000'},
            {'abbr': 'EOF', 'name': 'Esteban Ocon', 'team': 'FORCE INDIA MERCEDES', 'lap_time': '00:05:46.972000'},
            {'abbr': 'LHM', 'name': 'Lewis Hamilton', 'team': 'MERCEDES', 'lap_time': '00:06:47.540000'},
        ]
        fields = [ReportModel.abbr, ReportModel.name, ReportModel.team, ReportModel.lap_time]
        ReportModel.insert_many(data, fields).execute()
        response = self.client.get("/api/v2/report?order=asc")
        with self.subTest():
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers["Content-Type"], "application/json")
            self.assertEqual(response.json, (
                '[{"driver": "Sergey Sirotkin", "team": "WILLIAMS MERCEDES", "lap_time": ''"00:04:47.294000"},'
                ' {"driver": "Esteban Ocon", "team": "FORCE INDIA ''MERCEDES", "lap_time": "00:05:46.972000"},'
                ' {"driver": "Lewis Hamilton", ''"team": "MERCEDES", "lap_time": "00:06:47.540000"}]'))

    def test_report_desc(self):
        """src.report.monaco (converting_data.py) sorted the report by lap time"""
        data = [
            {'abbr': 'SSW', 'name': 'Sergey Sirotkin', 'team': 'WILLIAMS MERCEDES', 'lap_time': '00:04:47.294000'},
            {'abbr': 'EOF', 'name': 'Esteban Ocon', 'team': 'FORCE INDIA MERCEDES', 'lap_time': '00:05:46.972000'},
            {'abbr': 'LHM', 'name': 'Lewis Hamilton', 'team': 'MERCEDES', 'lap_time': '00:06:47.540000'},
        ]
        fields = [ReportModel.abbr, ReportModel.name, ReportModel.team, ReportModel.lap_time]
        ReportModel.insert_many(data, fields).execute()
        response = self.client.get("/api/v2/report?order=desc")
        with self.subTest():
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers["Content-Type"], "application/json")
            self.assertEqual(response.json, (
                '[{"driver": "Lewis Hamilton", ''"team": "MERCEDES", "lap_time": "00:06:47.540000"},'
                ' {"driver": "Esteban Ocon", "team": "FORCE INDIA ''MERCEDES", "lap_time": "00:05:46.972000"},'
                ' {"driver": "Sergey Sirotkin", "team": "WILLIAMS MERCEDES", "lap_time": ''"00:04:47.294000"}]'))

    def test_report_one_driver(self):
        """src.report.monaco (converting_data.py) sorted the report by lap time"""
        data = [
            {'abbr': 'SSW', 'name': 'Sergey Sirotkin', 'team': 'WILLIAMS MERCEDES', 'lap_time': '00:04:47.294000'},
            {'abbr': 'EOF', 'name': 'Esteban Ocon', 'team': 'FORCE INDIA MERCEDES', 'lap_time': '00:05:46.972000'},
            {'abbr': 'LHM', 'name': 'Lewis Hamilton', 'team': 'MERCEDES', 'lap_time': '00:06:47.540000'},
        ]
        fields = [ReportModel.abbr, ReportModel.name, ReportModel.team, ReportModel.lap_time]
        ReportModel.insert_many(data, fields).execute()
        response = self.client.get("/api/v2/report/drivers/driver=eof", query_string={"format": "json"})
        with self.subTest():
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers["Content-Type"], "application/json")
            self.assertEqual(response.json,
                             '{"driver": "Esteban Ocon", "team": "FORCE INDIA ''MERCEDES", "lap_time": "00:05:46.972000"}')

    def test_report_drivers(self):
        """src.report.monaco (converting_data.py) sorted the report by lap time"""
        data = [
            {'abbr': 'SSW', 'name': 'Sergey Sirotkin', 'team': 'WILLIAMS MERCEDES', 'lap_time': '00:04:47.294000'},
            {'abbr': 'EOF', 'name': 'Esteban Ocon', 'team': 'FORCE INDIA MERCEDES', 'lap_time': '00:05:46.972000'},
            {'abbr': 'LHM', 'name': 'Lewis Hamilton', 'team': 'MERCEDES', 'lap_time': '00:06:47.540000'},
        ]
        fields = [ReportModel.abbr, ReportModel.name, ReportModel.team, ReportModel.lap_time]
        ReportModel.insert_many(data, fields).execute()
        response = self.client.get("/api/v2/report/drivers", query_string={"format": "json"})
        with self.subTest():
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers["Content-Type"], "application/json")
            self.assertEqual(response.json, (
                '[{"abbr": "SSW", "diver": "Sergey Sirotkin"},'
                ' {"abbr": "EOF", "diver": "Esteban Ocon"},'
                ' {"abbr": "LHM", "diver": "Lewis Hamilton"}]'))
