#!/usr/bin/python3
'''Contains the places view for the API.'''
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
'''Methods for the states endpoint.'''


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    '''Gets the list of places in a city.
    '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=ALLOWED_METHODS, strict_slashes=False)
def handle_places(place_id):
    '''The method handler for the places endpoint.
    '''
    handlers = {
        'GET': get_place,
        'DELETE': remove_place,
        'POST': add_place,
        'PUT': update_place,
    }
    if request.method in handlers:
        return handlers[request.method](place_id)
    else:
        abort(405, description=f'Method {request.method} Not Allowed')


def get_place(place_id):
    '''Gets the place with the given id.
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


def remove_place(place_id):
    '''Removes a place with the given id.
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


def add_place(city_id):
    '''Adds a new place to a city.
    '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if type(data) is not dict:
        abort(400, description='Not a JSON')
    if 'user_id' not in data:
        abort(400, description='Missing user_id')
    if 'name' not in data:
        abort(400, description='Missing name')
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    new_place = Place(city_id=city.id, user_id=user.id, **data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


def update_place(place_id):
    '''Updates the place with the given id.
    '''
    xkeys = ('id', 'user_id', 'city_id', 'created_at', 'updated_at')
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if type(data) is not dict:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in xkeys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
