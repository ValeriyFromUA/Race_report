from flask_app import create_report_from_db


def report_sorting(order) -> list:
    if order == 'desc':
        return list(reversed(create_report_from_db()))
    return create_report_from_db()
