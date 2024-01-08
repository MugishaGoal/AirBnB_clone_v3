#!/usr/bin/python3
"""
State objects that handles all default RESTFul API actions
"""
from flask import jsonify, request
from api.v1.views import app_views
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from models import storage
from models.state import State

METHODS_ALLOWED = ['DELETE', 'GET', 'POST', 'PUT']
"""Methods allowed for the states"""


@app_views.route('/states', methods=METHODS_ALLOWED)
@app_views.route('/states/<state_id>', methodS=METHODS_ALLOWED)
def handle_states(state_id=None):
    """Handles methods for the states endpoint"""
    handlers = {
        'GET': get_states,
        'DELETE': remove_state,
        'POST': add_state,
        'PUT': update_state,
    }
    if request.method in handlers:
        return handlers[request.method](state_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_states(state_id=None):
    """
    Retrieves the list of states id or all states
    """
    all_states = storage.all(State).values()
    if state_id:
        request = list(filter(lambda x: x.id == state_id, all_states))
        if request:
            return jsonify(request[0].to_dict())
        raise NotFound()
    all_states = list(map(lambda x: x.to_dict(), all_states))
    return jsonify(all_states)


def delete_state(state_id=None):
    """Deletes a state object by id"""
    all_states = storage.all(State).values()
    request = list(filter(lambda x: x.id == state_id, all_states))
    if request:
        storage.delete(request[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def create_state(state_id=None):
    """Creates a new State object"""
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


def update_state(state_id=None):
    """Updates a State object by state_id"""
    keys = ('id', 'created_at', 'updated_at')
    all_states = storage.all(State).values()
    req = list(filter(lambda x: x.id == state_id, all_states))
    if req:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        old_state = req[0]
        for key, value in data.items():
            if key not in keys:
                setattr(old_state, key, value)
        old_state.save()
        return jsonify(old_state.to_dict()), 200
    raise NotFound()
