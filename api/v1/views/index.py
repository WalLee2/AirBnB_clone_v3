#!/usr/bin/python3
"""
Returning a JSON status
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slahes=False)
def json_status():
    """
    return the status OK
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slahes=False)
def count_cls_obj():
    """
    return the number of class objects within each class
    """
    return jsonify({"amenities": storage.count('Amenity'),
                    "cities": storage.count('City'),
                    "places": storage.count('Place'),
                    "reviews": storage.count('Review'),
                    "states": storage.count('State'),
                    "users": storage.count('User')})
