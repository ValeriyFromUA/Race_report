from flask_app.settings import APP, DEBUG, HOST, PORT

if __name__ == '__main__':
    APP.run(debug=DEBUG, host=HOST, port=PORT)
