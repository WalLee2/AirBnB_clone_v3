#!/usr/bin/python3
"""
Returning a JSON status
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def json_status():
    """
    return the status OK
    """
    return jsonify({"status": "OK"})
