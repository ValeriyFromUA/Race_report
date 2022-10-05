from __future__ import annotations

import json
from typing import Union

from flasgger import swag_from
from flask import Response, request, wrappers
from flask_restful import Resource

from .converting_data import (get_drivers_from_db, get_one_driver_from_db, get_report_from_db)
from .settings import API, VER
from .utils import report_sorting

ROUTE = f'/api/{VER}/report'


class ReportALL(Resource):
    @swag_from('swagger/report.yml', endpoint='report_order')
    def get(self) -> str:
        """Returns the report in ascending order unless descending (desc) is selected"""
        order = request.args.get('order')
        return json.dumps(report_sorting(order, get_report_from_db()))


API.add_resource(ReportALL, ROUTE, endpoint='report_order')


class ReportDrivers(Resource):
    @swag_from('swagger/report_all_drivers.yml', endpoint='report_all_drivers')
    def get(self) -> str:
        return json.dumps(get_drivers_from_db())


API.add_resource(ReportDrivers, f'{ROUTE}/drivers', endpoint='report_all_drivers')


class ReportOneDriver(Resource):
    @swag_from('swagger/report_driver.yml', endpoint='report_driver')
    def get(self, driver: str) -> Union[str, wrappers.Response]:
        if (walrus_driver := get_one_driver_from_db(driver)) is None:
            return Response('{"message": "Driver not found, please check abbreviation"}', status=404)
        return json.dumps(walrus_driver)


API.add_resource(ReportOneDriver, f'{ROUTE}/drivers/driver=<string:driver>',
                 endpoint='report_driver')
