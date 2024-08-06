#!/usr/bin/python3
'''Contains a Flask web application API.
'''
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
import os


app = Flask(__name__)
'''application started'''
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def tear_down(exception):
    '''tear down flask'''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''404 handle error'''
    return jsonify(error='Not found'), 404


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
