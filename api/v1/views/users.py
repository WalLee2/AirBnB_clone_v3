#!/usr/bin/python3
"""
API routes for User Objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Route: GET /api/v1/users """
    users = storage.all("User")
    users = [v.to_json() for k, v in users.items()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """ Route: GET /api/v1/users/<user_id> """
    user = storage.get("User", user_id)
    if (user is None):
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get("User", user_id)
    if (user is None):
        abort(404)

    storage.delete(user)
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    form_info = request.get_json()
    if not form_info:
        abort(400, 'Not a JSON')
    if 'email' not in form_info:
        abort(400, 'Missing email')
    if 'password' not in form_info:
        abort(400, 'Missing password')

    new_user = User(email=form_info.get('email'),
                    password=form_info.get('password'),
                    first_name=form_info.get('first_name'),
                    last_name=form_info.get('last_name'))
    storage.new(new_user)
    storage.save()
    user = storage.get("User", new_user.id)
    return jsonify(user.to_json()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    form_info = request.get_json()
    if not form_info:
        abort(400, 'Not a JSON')

    user.email = form_info.get('email', user.email)
    user.password = form_info.get('email', user.password)
    user.first_name = form_info.get('email', user.first_name)
    user.last_name = form_info.get('email', user.last_name)
    user.save()
    return jsonify(user.to_json())
