#!/usr/bin/env python3
""" Basic flask app """
from flask import (
        Flask,
        jsonify,
        request,
        abort,
        redirect,
        url_for
        )
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def message():
    """return a simple dict"""
    msg = {"message": "Bienvenue"}

    return jsonify(msg)


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """Register a user if not exist"""
    try:
        # Get email and password from the form data
        email = request.form.get("email")
        password = request.form.get("password")

        user = AUTH.register_user(email, password)

        response_data = {"email": user.email, "message": "user created"}

        return jsonify(response_data), 200
    except ValueError:
        response_data = {"message": "email already registered"}
        return jsonify(response_data), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """signing up as user"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    response = {"email": email, "message": "logged in"}
    json_response = jsonify(response)

    # create cookie for the response
    json_response.set_cookie("session_id", session_id)

    return json_response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """loging out a user"""
    session_id = request.cookies.get("session_id", None)

    user = AUTH.get_user_from_session_id(session_id)

    if session_id and user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ user profile """
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if user:
        response = {"email": user.email}
        return jsonify(response), 200
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Generate a token for resetting a user's password
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        response = {
                "email": email,
                "reset_token": reset_token
                }
        return jsonify(response)
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    Update a user's password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
        response = {
                "email": email,
                "message": "Password updated"
                }
        return jsonify(response)
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
