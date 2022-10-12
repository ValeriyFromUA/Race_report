import json
import unittest
from typing import List, Dict

from app import APP
from flask_app.models import ReportModel
from tests import MODELS, test_db


class ReportDBTest(unittest.TestCase):
    data = [
        {"abbr": "SSW", "name": "Sergey Sirotkin", "team": "WILLIAMS MERCEDES", "lap_time": "00:04:47.294000"},
        {"abbr": "EOF", "name": "Esteban Ocon", "team": "FORCE INDIA MERCEDES", "lap_time": "00:05:46.972000"},
        {"abbr": "LHM", "name": "Lewis Hamilton", "team": "MERCEDES", "lap_time": "00:06:47.540000"},
    ]

    def setUp(self):
        APP.testing = True
        self.client = APP.test_client()

        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

        fields = [ReportModel.abbr, ReportModel.name, ReportModel.team, ReportModel.lap_time]
        ReportModel.insert_many(self.data, fields).execute()

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def get_report_list(self) -> List[Dict]:
        report_list = []
        for el in self.data:
            report_data = {
                'driver': el['name'],
                'team': el['team'],
                'lap_time': el['lap_time']
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

    def test_report(self):
        """src.report.monaco (db_managers.py) sorted the report by lap time"""
        urls = ["/api/v2/report", "/api/v2/report?order=asc"]
        for url in urls:
            response = self.client.get(url)
            with self.subTest():
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json, json.dumps(self.get_report_list()))

    def test_report_desc(self):
        """src.report.monaco (db_managers.py) sorted the report by lap time"""
        response = self.client.get("/api/v2/report?order=desc")
        with self.subTest():
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, json.dumps(list(reversed(self.get_report_list()))))

    def test_report_one_driver(self):
        response = self.client.get("/api/v2/report/drivers/driver=eof")
        with self.subTest():
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json,
                             '{"driver": "Esteban Ocon", "team": "FORCE INDIA MERCEDES",'
                             ' "lap_time": "00:05:46.972000"}')

    def test_bad_report_one_driver(self):
        response = self.client.get("/api/v2/report/drivers/driver=xxx")
        with self.subTest():
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.decode('utf-8'),
                             '{"message": "Driver not found, please check abbreviation"}')

    def test_report_drivers(self):
        response = self.client.get("/api/v2/report/drivers")
        with self.subTest():
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, json.dumps(self.get_drivers_list()))
