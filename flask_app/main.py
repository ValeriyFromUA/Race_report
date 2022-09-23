import json
from flasgger import swag_from
from flask_restful import Resource
from flask_app import create_report_from_db

from flask_app.settings import ROUTE, API


class ReportALL(Resource):
    @swag_from('swagger/report.yml', endpoint='report')
    def get(self) -> json:
        return json.dumps(create_report_from_db())


API.add_resource(ReportALL, ROUTE, endpoint='report')


class ReportOrder(Resource):
    @swag_from('swagger/report_order.yml', endpoint='report_order')
    def get(self, order='asc') -> json:
        return json.dumps(list(reversed(create_report_from_db()))) if order == 'desc' else json.dumps(
            create_report_from_db())


API.add_resource(ReportOrder, f'{ROUTE}/order=<string:order>', endpoint='report_order')


class ReportOneDriver(Resource):
    @swag_from('swagger/report_driver.yml', endpoint='report_driver')
    def get(self, order='asc', driver=''):
        """Selection of static type and driver"""
        if driver != '':
            for line in create_report_from_db():
                if driver in line.values():
                    return json.dumps(line)
            return 'Driver_Not_Found'


API.add_resource(ReportOneDriver, f'{ROUTE}/order=<string:order>/driver=<string:driver>',
                 endpoint='report_driver')
