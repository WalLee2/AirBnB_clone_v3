#!/usr/bin/python3
"""
Handle all default RESTful API actions for City class
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.base_model import BaseModel
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """
    Get all cities from a particular state
    """
    if state_id is None:
        return (abort(404))
    found_city = []
    my_state = storage.get("State", state_id)
    if my_state is None:
        return (abort(404))
    all_cities = storage.all("City")
    for k, v in all_cities.items():
        if v.state_id == state_id:
            found_city.append(v.to_json())
    return jsonify(found_city)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def one_city(city_id):
    """
    Get one city based off of the given id
    """
    city = storage.get("City", city_id)
    if city is not None:
        city = city.to_json()
        return jsonify(city)
    else:
        return (abort(404))


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Delete the city based off of the city_id
    """
    if storage.get("City", city_id) is not None:
        storage.delete(storage.get("City", city_id))
        return (jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Create the city with the given state_id
    """
    state = storage.get("State", state_id)
    data = request.get_json()
    if state is None:
        return abort(404)
    if not data:
        return (abort(400), 'Not a JSON')
    elif data.get("name") is None:
        return (abort(400), 'Missing name')
    else:
        data["state_id"] = state_id
        new_city = City(data)
        storage.new(new_city)
        storage.save()
        my_city = storage.get("City", new_city.id)
        return (jsonify(my_city.to_json()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Update the existing city with the correct id
    """
    city = storage.get("City", city_id)
    data = request.get_json()
    if city is None:
        return abort(404)
    if data is None:
        return abort(400), 'Not a JSON'
    city.name = data.get('name', city.name)
    city.save()
    return jsonify(city.to_json())
