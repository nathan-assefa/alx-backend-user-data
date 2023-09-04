#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPE = os.environ.get("AUTH_TYPE")

if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unathorized(error) -> str:
    """ unathorized error """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ forbiden  error """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request_handler():
    '''
    This method would be called before any request
    is served, and this is helpful to check if the request
    is authorized and not forbidden, and so on.
    '''
    if not auth:
        return
    # This paths are excluded paths
    excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/'
            ]
    
    # here using the request_auth method, we first check if
    # + request.path is not in excluded paths
    if not auth.require_auth(request.path, excluded_paths):
        return
    
    # we then check if the request contains the header
    # + authorization
    if not auth.authorization_header(request):
        abort(401)

    if not auth.current_user(request):
        abort(403)




if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
