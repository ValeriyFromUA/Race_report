from flask_app import *
from flask_app.settings import *

if __name__ == '__main__':
    APP.run(debug=DEBUG, host=HOST, port=PORT)
