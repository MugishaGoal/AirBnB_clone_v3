#!/usr/bin/python3
'''Contains the reviews views for the API.'''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_reviews(place_id=None, review_id=None):
    '''The method handlers of the reviews endpoint.
    '''
    managers = {
        'GET': get_reviews,
        'DELETE': remove_review,
        'POST': add_review,
        'PUT': update_review
    }
    if request.method in managers:
        return managers[request.method](place_id, review_id)
    else:
        abort(405)


def get_reviews(place_id=None, review_id=None):
    '''Gets the review by the given id or all reviews in
    the place by the given id.
    '''
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            all_reviews = place.reviews
            reviews = list(map(lambda x: x.to_dict(), all_reviews))
            return jsonify(reviews)
    elif review_id:
        review = storage.get(Review, review_id)
        if review:
            return jsonify(review.to_dict())
    abort(404)


def remove_review(place_id=None, review_id=None):
    '''Removes a review by the given id.
    '''
    if review_id:
        review = storage.get(Review, review_id)
        if review:
            storage.delete(review)
            storage.save()
            return jsonify({}), 200
    abort(404)


def add_review(place_id=None, review_id=None):
    '''Adds a new review.
    '''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if type(data) is not dict:
        abort(400, description='Not a JSON')
    if 'user_id' not in data:
        abort(400, description='Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'text' not in data:
        abort(400, description='Missing text')
    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


def update_review(place_id=None, review_id=None):
    '''Updates the review by the given id.
    '''
    un_keys = ('id', 'user_id', 'place_id', 'created_at', 'updated_at')
    review = storage.get(Review, review_id)
    if review:
        data = request.get_json()
        if type(data) is not dict:
            abort(400, description='Not a JSON')
        for key, value in data.items():
            if key not in un_keys:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    abort(404)
