#!/usr/bin/python3
'''Contains the places_amenities views for the API.'''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET', 'POST'])
@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def handle_places_amenities(place_id=None, amenity_id=None):
    '''The method handlers of the places_amenities endpoint.
    '''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)

    if request.method == 'GET':
        return get_amenities(place)
    elif request.method == 'DELETE':
        return remove_amenity(place, amenity)
    elif request.method == 'POST':
        return add_amenity(place, amenity)
    abort(405)


def get_amenities(place):
    '''Gets the amenities linked to the place.
    '''
    if storage_type == 'db':
        amenities = list(place.amenities)
    else:
        amenities = []
        for amenity_id in place.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenities.append(amenity)
    amenities = list(map(lambda x: x.to_dict(), amenities))
    return jsonify(amenities)


def remove_amenity(place, amenity):
    '''Removes an amenity linked to the place.
    '''
    if not amenity:
        abort(404)
    if storage_type == 'db':
        if amenity in place.amenities:
            place.amenities.remove(amenity)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)
    else:
        if amenity.id in place.amenity_ids:
            place.amenity_ids.remove(amenity.id)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)


def add_amenity(place, amenity):
    '''Links an amenity to the place.
    '''
    if not amenity:
        abort(404)

    if storage_type == 'db':
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            storage.save()
            return jsonify(amenity.to_dict()), 201
        else:
            return jsonify(amenity.to_dict()), 200
    else:
        if amenity.id not in place.amenity_ids:
            place.amenity_ids.append(amenity.id)
            storage.save()
            return jsonify(amenity.to_dict()), 201
        else:
            return jsonify(amenity.to_dict()), 200
