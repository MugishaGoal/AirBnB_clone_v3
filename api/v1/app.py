#!/usr/bin/python3
"""A flask web application API"""
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
"""A Flask Web application instance"""
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(exception):
    """The Flask request end event listener"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
