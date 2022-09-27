import json

from flask import Response

from flask_app import create_report_from_db


def report_sorting(order):
    if order == 'desc':
        return json.dumps(list(reversed(create_report_from_db()[0])))
    return json.dumps(create_report_from_db()[0])


def driver_choosing(abbr=None):
    if abbr:
        for line in create_report_from_db()[0]:
            if abbr.upper() in line.keys():
                return json.dumps(line)
        return Response("Driver not found, please check abbreviation", status=404)
