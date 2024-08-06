#!/usr/bin/python3
'''application file contain Flask application API
'''

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
'''The flask app created'''
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exception):
    '''the flask teardown to close storage'''
    storage.close()

@app.errorhandler(404)
def not_found(err):
    '''handle not found 404 http error code'''
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", threaded=True)
