#!/usr/bin/python3
"""
Handles RESTful API actions for State object
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.base_model import BaseModel
from models import storage
from api.v1.app import not_found
from models.state import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def get_all_state():
    """
    function that grabs all the state objects and returns a JSON list
    """
    states = storage.all("State")
    states = [v.to_json() for k, v in states.items()]
    return jsonify(states)

@app_views.route('/states/<id>', methods=['GET'])
def get_specific_state(id):
    """
    Gets a state with it's specific ID and returns a JSON object
    to_json() is a method called from BaseModel that converts
    to a dictionary and then jsonify converts it into a proper JSON file
    """
    if (storage.get("State", id) is not None):
        return (jsonify(storage.get("State", id).to_json()))
    else:
        return (not_found(404))

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Checks if the state object associated with the ID exists.
    Delete it if it exists or return if it's not found
    """
    if (storage.get("State", state_id) is None):
        return (not_found(404))
    storage.delete(storage.get("State", state_id))
    return (jsonify({}), 200)

@app_views.route('/states/', methods=['POST'])
def create_state():
    """
    Use request.get_json to convert the HTTP body into a dictionary.
    Return a proper JSON object if data is not an error
    """
    data = request.get_json()
    if not data:
        return (abort(400, 'Not a JSON'))
    elif data.get("name") is None:
        return (abort(400, 'Missing name'))
    else:
        new_state = State(name=data['name'])
        storage.new(new_state)
        my_state = storage.get("State", new_state.id)
        storage.save()
        return (jsonify(my_state.to_json()), 201)


@app_views.route('/states/<id>', methods=['PUT'])
def update_state(id):
    """
    Update the State object with all key value pairs of the dictionary
    """
    state_dict = storage.get("State", id)
    if state_dict is None:
        return not_found(404)
    check = request.get_json()
    if check is None:
        return (abort(400), 'Not a JSON')
    dict_value = state_dict
    dict_value.name = check.get('name', dict_value.name)
    dict_value.save()
    return (jsonify(dict_value.to_json()))
