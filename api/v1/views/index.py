import app_views from api.v1.views


@app_views.route('/status')
def json_status():
    return json.dumps({"status": "OK"})
