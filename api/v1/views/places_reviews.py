#!/usr/bin/python3
"""
API routes for Reviews Objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """ GET /api/v1/places/<place_id>/reviews """
    place = storage.get("Place", place_id)
    if (place is None):
        abort(404)

    place_reviews = []
    reviews = [v.to_json() for k, v in storage.all("Review").items()]
    for review in reviews:
        if place_id == review['place_id']:
            place_reviews.append(review)

    return jsonify(place_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Route: GET /api/v1/reviews/<review_id> """
    review = storage.get("Review", review_id)
    if (review is None):
        abort(404)

    return jsonify(review.to_json())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Route: DELETE /api/v1/reviews/<review_id> """
    review = storage.get("Review", review_id)
    if (review is None):
        abort(404)

    storage.delete(review)
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """ Route: POST /api/v1/places/<place_id>/reviews """
    place = storage.get("Place", place_id)
    if (place is None):
        abort(404)

    form_info = request.get_json()
    if not form_info:
        abort(400, 'Not a JSON')
    if 'user_id' not in form_info:
        abort(400, 'Missing user_id')

    user = storage.get("User", form_info.get('user_id'))
    if (user is None):
        abort(404)

    if 'text' not in form_info:
        abort(400, 'Missing text')

    new_review = Review(place_id=place_id,
                        user_id=form_info.get('user_id'),
                        text=form_info.get('text'))
    storage.new(new_review)
    storage.save()
    return (jsonify(new_review.to_json()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """ Route: PUT /api/v1/reviews/<review_id> """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    form_info = request.get_json()
    if not form_info:
        abort(400, 'Not a JSON')

    review.text = form_info.get('text', review.text)
    return (jsonify(review.to_json()), 200)
