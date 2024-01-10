#!/usr/bin/python3
'''Contains the users views for the API.'''
from flask import jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']


@app_views.route('/users', methods=ALLOWED_METHODS)
@app_views.route('/users/<user_id>', methods=ALLOWED_METHODS)
def handle_users(user_id=None):
    '''The method handlers of the users endpoint.
    '''
    managers = {
        'GET': get_users,
        'DELETE': remove_user,
        'POST': add_user,
        'PUT': update_user,
    }
    if request.method in managers:
        return managers[request.method](user_id)
    else:
        abort(405, description=f'Method {request.method} Not Allowed')


def get_users(user_id=None):
    '''Gets the user by the given id or all users.
    '''
    all_users = storage.all(User).values()
    if user_id:
        res = list(filter(lambda x: x.id == user_id, all_users))
        if res:
            return jsonify(res[0].to_dict())
        abort(404)
    all_users = list(map(lambda x: x.to_dict(), all_users))
    return jsonify(all_users)


def remove_user(user_id=None):
    '''Removes a user by the given id.
    '''
    all_users = storage.all(User).values()
    result = list(filter(lambda x: x.id == user_id, all_users))
    if result:
        storage.delete(result[0])
        storage.save()
        return jsonify({}), 200
    abort(404)


def add_user(user_id=None):
    '''Adds a new user.
    '''
    data = request.get_json()
    if type(data) is not dict:
        abort(400, description='Not a JSON')
    if 'email' not in data:
        abort(400, description='Missing email')
    if 'password' not in data:
        abort(400, description='Missing password')
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


def update_user(user_id=None):
    '''Updates the user by the given id.
    '''
    un_keys = ('id', 'email', 'created_at', 'updated_at', 'password')
    all_users = storage.all(User).values()
    result = list(filter(lambda x: x.id == user_id, all_users))
    if result:
        data = request.get_json()
        if type(data) is not dict:
            abort(400, description='Not a JSON')
        old_user = result[0]
        for key, value in data.items():
            if key not in un_keys:
                setattr(old_user, key, value)
        old_user.save()
        return jsonify(old_user.to_dict()), 200
    abort(404)
