from unittest import TestCase

from flask_app.utils import report_sorting


class TestReportSorting(TestCase):
    data = [{'1': '2', '3': '4'}, {'5': '6', '7': '8'}, {'9': '10'}]

    def test_report_asc(self):
        self.assertEqual(report_sorting('asc_or_something_else', self.data), self.data)

    def test_report_desc(self):
        self.assertEqual(report_sorting('desc', self.data),
                         [{'9': '10'}, {'5': '6', '7': '8'}, {'1': '2', '3': '4'}])
