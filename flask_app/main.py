from flasgger import swag_from
from flask_restful import Resource

from flask_app import create_report_from_db

from flask_app.settings import VER, API


class ReportALL(Resource):
    @swag_from('swagger/report.yml', endpoint='report')
    def get(self):
        return create_report_from_db()


API.add_resource(ReportALL, f'/api/{VER}/report', endpoint='report')


class ReportOrder(Resource):
    @swag_from('swagger/report_order.yml', endpoint='report_order')
    def get(self, order='asc'):
        return list(reversed(create_report_from_db())) if order == 'desc' else create_report_from_db()


API.add_resource(ReportOrder, f'/api/{VER}/report/order=<string:order>', endpoint='report_order')


class ReportOneDriver(Resource):
    @swag_from('swagger/report_driver.yml', endpoint='report_driver')
    def get(self, order='asc', driver=''):
        # selection of static type and driver
        if driver:
            for line in create_report_from_db():
                if driver in line:
                    return list(line)
            return 'Driver_Not_Found', 404


API.add_resource(ReportOneDriver, f'/api/{VER}/report/order=<string:order>/driver=<string:driver>',
                 endpoint='report_driver')
