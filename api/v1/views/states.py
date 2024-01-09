#!/usr/bin/python3
"""Contains the states view for the API"""
from flask import jsonify, request
from api.v1.views import app_views
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from models import storage
from models.state import State


ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
"""Methods for the states endpoint"""


@app_views.route('/states', methods=ALLOWED_METHODS)
@app_views.route('/states/<state_id>', methods=ALLOWED_METHODS)
def manage_states(state_id=None):
    """Retrieve the list of all State objects"""
    managers = {
        'GET': get_states,
        'DELETE': remove_state,
        'POST': add_state,
        'PUT': update_state,
    }
    if request.method in managers:
        return managers[request.method](state_id)
    else:
        raise MethodNotAllowed(list(managers.keys()))


def get_states(state_id=None):
    """Retrieve a State object by state_id"""
    all_states = storage.all(State).values()
    if state_id:
        result = list(filter(lambda x: x.id == state_id, all_states))
        if result:
            return jsonify(result[0].to_dict())
        raise NotFound()
    all_states = list(map(lambda x: x.to_dict(), all_states))
    return jsonify(all_states)


def delete_state(state_id=None):
    """Delete a State object by state_id"""
    all_states = storage.all(State).values()
    result = list(filter(lambda x: x.id == state_id, all_states))
    if result:
        storage.delete(result[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def create_state(state_id=None):
    """Create a new State object"""
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


def update_state(state_id=None):
    """Update a state object by state_id"""
    xkeys = ('id', 'created_at', 'updated_at')
    all_states = storage.all(State).values()
    res = list(filter(lambda x: x.id == state_id, all_states))
    if res:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        old_state = res[0]
        for key, value in data.items():
            if key not in xkeys:
                setattr(old_state, key, value)
        old_state.save()
        return jsonify(old_state.to_dict()), 200
    raise NotFound()
