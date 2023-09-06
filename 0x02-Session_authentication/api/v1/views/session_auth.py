#!/usr/bin/env python3
""" Module of auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def auth_session_login() -> str:
    """handling login"""
    # get the email and password from request
    email = request.form.get("email", None)
    password = request.form.get("password", None)

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve the User instance based on the email
    user_list = User.search({"email": email})

    # Check if no User found
    if not user_list:
        return jsonify({"error": "no user found for this email"}), 404

    for user in user_list:
        # Check if the password is not the one of the User
        if user.is_valid_password(password):
            from api.v1.app import auth
            from os import getenv

            # Create a Session ID for the User ID
            session_id = auth.create_session(user.id)

            # Return the dictionary representation of the User
            user_dict = jsonify(user.to_json())

            # set cookie values
            cookie_name = getenv("SESSION_NAME")
            cookie_value = session_id
            user_dict.set_cookie(cookie_name, cookie_value)

            return user_dict
        else:
            return jsonify({"error": "wrong password"}), 401


@app_views.route(
        "/auth_session/logout", methods=["DELETE"], strict_slashes=False
        )
def session_logout():
    """Logging out of the session"""
    from api.v1.app import auth

    removed_session = auth.destroy_session(request)

    if not removed_session:
        abort(404)
    return jsonify({}), 200
