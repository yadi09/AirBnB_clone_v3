#!/usr/bin/python3
'''Index application route to status.'''
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return status ok"""
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stat():
    """return number of each class object"""
    return jsonify(
        amenities=storage.count('Amenity'),
        cities=storage.count('City'),
        places=storage.count('Place'),
        reviews=storage.count('Review'),
        states=storage.count('State'),
        users=storage.count('User')
    )
