#!/usr/bin/python3
"""
Handle all default RESTful API actions for City class
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.base_model import BaseModel
from models import storage
from api.v1.app import not_found
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_all_cities(state_id):
    """

    """
    if state_id is None:
        return (not_found(404))
    found_city = []
    my_state = storage.get("State", state_id)
    if my_state is None:
        return (not_found(404))
    all_cities = storage.all("City")
    for k, v in all_cities.items():
        if v.state_id == state_id:
            found_city.append(v.to_json())
    return jsonify(found_city)

@app_views.route('/cities/<city_id>', methods=['GET'])
def check_city_id(city_id):
    """

    """
    if storage.get("City", city_id) is not None:
        return (jsonify(storage.get("City", city_id)[city_id].to_json))
    else:
        return (abort(404))
