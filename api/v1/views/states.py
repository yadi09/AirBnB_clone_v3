#!/usr/bin/python3
'''state object serve module'''

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, make_response, jsonify, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    '''Retrieves all list of state'''
    states = storage.all(State)
    return jsonify([obj.to_dict() for obj in states.values()])

@app_views.route('/states/<state_id>')
def state(state_id):
    '''single state retrive by id'''
    states = storage.all(State)
    for key in states:
        if state_id in key:
            return jsonify(states[key].to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    '''delete state object by id'''
    states = storage.all(State)
    for key in states:
        if state_id in key:
            states[key].delete()
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    '''post(create) new state with status-201'''
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    if 'name' not in new_state:
        abort(400, "Missing name")
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    '''Updates a State object'''
    state = storage.all(State)
    obj = None
    for key in state:
        if state_id in key:
            obj = state[key]
    if not obj:
        abort(404)

    reqst = request.get_json()
    if not reqst:
        abort(400, "Not a JSON")

    for key, value in reqst.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(obj, key, value)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
