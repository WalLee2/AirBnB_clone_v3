#!/usr/bin/python3
"""
Running flask on local host and on port 5000
"""
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
"""
cors = CORS(app, resources={r"/api/*":
                            {
                                "origins": getenv("HBNB_API_HOST", "0.0.0.0")
                            }})
"""

@app.teardown_appcontext
def app_teardown(exception):
    """
    teardown after use
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return (jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    my_host = '0.0.0.0'
    my_port = '5000'
    if getenv(HBNB_API_HOST):
        my_host = getenv("HBNB_API_HOST")
    if getenv(HBNB_API_PORT):
        my_port = getenv("HBNB_API_PORT")
    app.run(host=my_host, port=my_port)
