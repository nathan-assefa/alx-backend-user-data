#!/usr/bin/env python3
""" Basic flask app """
from flask import (
        Flask,
        jsonify,
        request,
        abort,
        redirect,
        make_response,
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

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user:
        AUTH.destroy_session(user.id)

        response = make_response(redirect(url_for("/")))

        response.delete_cookie("session_id")

        return redirect("/")
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
