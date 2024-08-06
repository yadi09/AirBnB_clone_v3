#!/usr/bin/python3
"""amenity blueprint"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def amnty():
    """return list of obj"""
    amnty = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in amnty.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity(amenity_id):
    """return single amenity"""
    amnty = storage.get(Amenity, amenity_id)
    if not amnty:
        abort(404)
    return jsonify(amnty.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amnty(amenity_id):
    """delete amnty"""
    amnty = storage.get(Amenity, amenity_id)
    if not amnty:
        abort(404)

    amnty.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amnty():
    """create amnty"""
    amnty = request.get_json()
    if not amnty:
        abort(400, "Not a JSON")
    if 'name' not in amnty:
        abort(400, "Missing name")

    new = Amenity(**amnty)
    storage.new(new)
    storage.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amnty(amenity_id):
    """update amnty"""
    amnty = storage.get(Amenity, amenity_id)
    if not amnty:
        abort(404)

    update = request.get_json()
    if not update:
        abort(400, "Not a JSON")

    for key, value in update.items():
        if key not in ['id', 'created_at', 'update_at']:
            setattr(amnty, key, value)

    storage.save()
    return make_response(jsonify(amnty.to_dict()), 200)
