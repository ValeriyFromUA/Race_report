from flask import Flask
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from
from app.converting_data import create_report_from_db

VER = 'v2'
app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)


class Report(Resource):
    @swag_from('swagger/report.yml', endpoint='report')
    @swag_from('swagger/report_order.yml', endpoint='report_order')
    @swag_from('swagger/report_driver.yml', endpoint='report_driver')
    def get(self, order='asc', driver=''):
        # selection of data type and driver
        if driver:
            for line in create_report_from_db():
                if driver in line:
                    return list(line)
        return list(reversed(create_report_from_db())) if order == 'desc' else create_report_from_db()


api.add_resource(Report, f'/api/{VER}/report', endpoint='report')
api.add_resource(Report, f'/api/{VER}/report/order=<string:order>', endpoint='report_order')
api.add_resource(Report, f'/api/{VER}/report/order=<string:order>/driver=<string:driver>', endpoint='report_driver')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
