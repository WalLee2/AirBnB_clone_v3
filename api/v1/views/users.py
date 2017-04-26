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


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Route: GET /api/v1/users/<user_id> """
    user = storage.get("User", user_id)
    if (user is None):
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Route: DELETE /api/v1/users/<user_id> """
    user = storage.get("User", user_id)
    if (user is None):
        abort(404)
    storage.delete(user)
    return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Route: POST /api/v1/users """
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
    return (jsonify(new_user.to_json()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Route: PUT /api/v1/users/<user_id> """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    form_info = request.get_json()
    if not form_info:
        abort(400, 'Not a JSON')

    user.password = form_info.get('email', user.password)
    user.first_name = form_info.get('email', user.first_name)
    user.last_name = form_info.get('email', user.last_name)
    user.save()
    return (jsonify(user.to_json()), 200)
