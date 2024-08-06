#!/usr/bin/python3
'''application file contain Flask application API
'''
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
'''The flask app created'''
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def tear_down(exception):
    '''the flask teardown to close storage'''
    storage.close()

@app.errorhandler(404)
def not_found(err):
    '''handle not found 404 http error code'''
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=app_host, port=app_port, threaded=True)
