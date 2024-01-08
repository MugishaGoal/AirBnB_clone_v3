#!/usr/bin/python3
"""A flask web application API"""
import os
from flask import Flask

from models import storage
from api.v1.views import app_views


app = Flask(__name__)
"""A Flask Web application instance"""
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """The Flask request end event listener"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """Handles 404 errors and returns a JSON-formatted 404 response."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def error_400(error):
    '''Handles the 400 HTTP error code.'''
    message = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        message = error.description
    return jsonify(error=message), 400


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
