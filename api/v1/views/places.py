#!/usr/bin/python3
"""
API routes for Place Objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """ Route: GET /api/v1/cities/<city_id>/places """
    city = storage.get("City", city_id)
    if (city is None):
        abort(404)

    city_places = []
    places = [v.to_json() for k, v in storage.all("Place").items()]
    for place in places:
        if city_id == place['city_id']:
            city_places.append(place)

    return jsonify(city_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Route: GET /api/v1/places/<place_id> """
    place = storage.get("Place", place_id)
    if (place is None):
        abort(404)

    return jsonify(place.to_json())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Route: DELETE /api/v1/places/<place_id> """
    place = storage.get("Place", place_id)
    if (place is None):
        abort(404)

    storage.delete(place)
    return jsonify({})


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Route: POST /api/v1/cities/<city_id>/places """
    city = storage.get("City", city_id)
    if (city is None):
        abort(404)

    form_info = request.get_json()
    if not form_info:
        abort(400, 'Not a JSON')
    if 'user_id' not in form_info:
        abort(400, 'Missing user_id')

    user = storage.get("User", form_info.get('user_id'))
    if (user is None):
        abort(404)

    if 'name' not in form_info:
        abort(400, 'Missing name')

    # Probably can refactor this to send in *args vs **kwargs
    # What is the issue that might occur for columns that cannot be null?
    new_place = Place(city_id=city_id,
                      user_id=form_info.get('user_id'),
                      name=form_info.get('name'),
                      description=form_info.get('description'),
                      number_rooms=form_info.get('number_rooms'),
                      number_bathrooms=form_info.get('number_bathrooms'),
                      max_guest=form_info.get('max_guest'),
                      price_by_night=form_info.get('price_by_night'),
                      latitude=form_info.get('latitude'),
                      longitude=form_info.get('longitude'))
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_json()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Route: PUT /api/v1/places/<place_id> """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    form_info = request.get_json()
    if not form_info:
        abort(400, 'Not a JSON')

    place.name = form_info.get('name', place.name)
    place.description = form_info.get('description', place.description)
    place.number_rooms = form_info.get('number_rooms', place.number_rooms)
    place.number_bathrooms = form_info.get('number_bathrooms',
                                           place.number_bathrooms)
    place.max_guest = form_info.get('max_guest', place.max_guest)
    place.price_by_night = form_info.get('price_by_night',
                                         place.price_by_night)
    place.latitude = form_info.get('latitude', place.latitude)
    place.longitude = form_info.get('longitude', place.longitude)
    place.save()

    return jsonify(place.to_json())
