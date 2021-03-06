#!/usr/bin/python3
"""
API routes for Amenity Objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Route: GET /api/v1/amenities """
    amenities = storage.all("Amenity")
    amenities = [v.to_json() for k, v in amenities.items()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Route: GET /api/v1/amenities/<amenity_id> """
    amenity = storage.get("Amenity", amenity_id)
    if (amenity is None):
        abort(404)
    return jsonify(amenity.to_json())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Route: DELETE /api/v1/amenities/<amenity_id> """
    amenity = storage.get("Amenity", amenity_id)
    if (amenity is None):
        abort(404)

    storage.delete(amenity)
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Route: POST /api/v1/amenities """
    form_info = request.get_json()
    if not form_info:
        abort(400, 'Not a JSON')
    if 'name' not in form_info:
        abort(400, 'Missing name')

    new_amenity = Amenity(name=form_info['name'])
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_json()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Route: PUT /api/v1/amenities/<amenity_id> """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    form_info = request.get_json()
    if not form_info:
        abort(400, 'Not a JSON')

    amenity.name = form_info.get('name', amenity.name)
    amenity.save()
    return jsonify(amenity.to_json())
