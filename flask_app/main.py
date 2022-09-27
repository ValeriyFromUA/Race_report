import json

from flasgger import swag_from
from flask import request
from flask_restful import Resource

from flask_app import create_report_from_db
from flask_app.settings import API, VER
from flask_app.utils import driver_choosing, report_sorting

ROUTE = f'/api/{VER}/report'


class ReportALL(Resource):
    @swag_from('swagger/report.yml', endpoint='report_order')
    def get(self) -> json:
        """Returns the report in ascending order unless descending (desc) is selected"""
        order = request.args.get('order')
        return report_sorting(order)


API.add_resource(ReportALL, ROUTE, endpoint='report_order')


class ReportDrivers(Resource):
    @swag_from('swagger/report_all_drivers.yml', endpoint='report_all_drivers')
    def get(self) -> json:
        return json.dumps(create_report_from_db()[1])


API.add_resource(ReportDrivers, f'{ROUTE}/drivers', endpoint='report_all_drivers')


class ReportOneDriver(Resource):
    @swag_from('swagger/report_driver.yml', endpoint='report_driver')
    def get(self, driver=None) -> json:
        return driver_choosing(driver)


API.add_resource(ReportOneDriver, f'{ROUTE}/drivers/driver=<string:driver>',
                 endpoint='report_driver')
