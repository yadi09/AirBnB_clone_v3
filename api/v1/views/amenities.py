#!/usr/bin/python3
"""amnty module documentation"""

from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, make_response, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amnty():
    '''amnty document get'''
    amntys = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in amntys.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amnty(amenity_id):
    '''one amnty only'''
    amnty = storage.get(Amenity, amenity_id)
    if not amnty:
        abort(404)
    return jsonify(amnty.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amnty(amenity_id):
    '''delete amnty'''
    amnty = storage.get(Amenity, amenity_id)
    if not amnty:
        abort(404)

    amnty.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amnty():
    '''create new amnty'''
    new = request.get_json()
    if not new:
        abort(400, "Not a JSON")
    if 'name' not in new:
        abort(400, "Missing name")
    new_amnty = Amenity(**new)
    storage.new(new_amnty)
    storage.save()
    return make_response(jsonify(new_amnty.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amnty(amenity_id):
    '''update amnty'''
    amnty = storage.get(Amenity, amenity_id)
    if not amnty:
        abort(404)
    new = request.get_json()
    if not new:
        abort(400, "Not a JSON")
    for key, value in new.items():
        if key not in ['id', 'created_at', 'update_at']:
            setattr(amnty, key, value)
    storage.save()
    return make_response(jsonify(amnty.to_dict()), 200)
