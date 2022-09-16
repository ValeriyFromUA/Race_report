from pathlib import Path

START = 'start.log'
END = 'end.log'
ABBREVIATIONS = 'abbreviations.txt'

# static/db settings
DATA_FOLDER_IN_APP = 'static'
APP_FOLDER = Path(__file__).resolve().parent
path = Path(APP_FOLDER / DATA_FOLDER_IN_APP)
