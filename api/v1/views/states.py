#!/usr/bin/python3
"""
State objects that handles all default RESTFul API actions
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request


METHODS_ALLOWED = ['GET', 'DELETE', 'POST', 'PUT']
"""Metods allowed"""


@app_views.route('/states', method=METHODS_ALLOWED, strict_slashes=False)
@app_views.route('/states/<state_id>', methods=METHODS_ALLOWED)
def get_all_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


def get_state_by_id(state_id):
    """Retrieves a State object by state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


def delete_state(state_id):
    """Deletes a State object by state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


def create_state():
    """Creates a new State object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


def update_state(state_id):
    """Updates a State object by state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
