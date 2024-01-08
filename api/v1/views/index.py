#!/usr/bin/python3
"""Contains a view index for the API"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Gets the status of the API"""
    return jsonify({"status": "OK"})
