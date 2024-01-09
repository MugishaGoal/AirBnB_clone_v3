#!/usr/bin/python3
"""State views module"""
from flask import jsonify, request
from api.v1.views import app_views
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from models import storage
from models.state import State


METHODS_ALLOWED = ['GET', 'DELETE', 'POST', 'PUT']
"""Methods for states endpoint"""


@app_views.route('/states', methods=METHODS_ALLOWED)
@app_views.route('/states/<state_id>', methods=METHODS_ALLOWED)
def manage_states(state_id=None):
    """The method handls the states endpoint"""
    managers = {
        'GET': get_states,
        'DELETE': remove_state,
        'POST': add_state,
        'PUT': update_state,
    }
    
    method = request.method
    if method in managers:
        return managers[method](state_id)
    else:
        raise MethodNotAllowed(list(managers.keys()))


def get_states(state_id=None):
    """Retrieve a State object by state_id"""
    all_states = storage.all(State).values()
    
    if state_id:
        result = next((x.to_dict() for x in all_states if x.id == state_id), None)
        if result:
            return jsonify(result)
        raise NotFound()
    
    all_states = [x.to_dict() for x in all_states]
    return jsonify(all_states)


def delete_state(state_id=None):
    """Delete a State object by state_id"""
    all_states = storage.all(State).values()
    state_to_delete = next((x for x in all_states if x.id == state_id), None)
    
    if state_to_delete:
        storage.delete(state_to_delete)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def create_state(state_id=None):
    """Create a new state object"""
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


def update_state(state_id=None):
    """Update a State object by state_id"""
    xkeys = ('id', 'created_at', 'updated_at')
    all_states = storage.all(State).values()
    old_state = next((x for x in all_states if x.id == state_id), None)
    
    if old_state:
        data = request.get_json()
        if not isinstance(data, dict):
            raise BadRequest(description='Not a JSON')
        
        for key, value in data.items():
            if key not in xkeys:
                setattr(old_state, key, value)
        
        old_state.save()
        return jsonify(old_state.to_dict()), 200
    
    raise NotFound()
