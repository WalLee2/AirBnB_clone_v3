#!/usr/bin/python3
"""

"""
import flask from Flask
import storage from models
import app_views from api.v1.views


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def app_teardown():
    storage.close()

if __name__ == "__main__":
    HBNB_API_HOST = 0.0.0.0
    HBNB_API_PORT = 5000
    flask run --host=HBNB_API_HOST --port=HBNB_API_PORT
