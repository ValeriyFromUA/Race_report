import os
import sys

module_path = os.path.abspath(os.getcwd() + '\\..')
if module_path not in sys.path:
    sys.path.append(module_path)
from flask_app import create_db_report

if __name__ == '__main__':
    create_db_report()
