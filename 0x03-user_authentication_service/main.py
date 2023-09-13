#!/usr/bin/env python3
""" user authentication """
import requests


BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """ registering a user """
    response = requests.post(
            f"{BASE_URL}/users", data={"email": email, "password": password}
            )
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """ Trying to log in with wrong password """
    response = requests.post(
            f"{BASE_URL}/sessions", data={"email": email, "password": password}
            )
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Logging a user with correct password """
    response = requests.post(
            f"{BASE_URL}/sessions", data={"email": email, "password": password}
            )
    assert response.status_code == 200
    return response.json().get("session_id")


def profile_unlogged() -> None:
    """ Sends a GET request to the profile endpoint without providing a
        session ID cookie. It expects an HTTP 403 status code,
        indicating unauthorized access.
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Sends a GET request to the profile endpoint with a session_id
    cookie to access a user's profile.
    """
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200
    # Validate the expected JSON payload here


def log_out(session_id: str) -> None:
    """ Logging out a user """
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 302


def reset_password_token(email: str) -> str:
    """ Reseting a user password """
    response = requests.post(
            f"{BASE_URL}/reset_password", data={"email": email}
            )
    assert response.status_code == 200
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Updating a user password """
    data = {
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
            }
    response = requests.put(f"{BASE_URL}/reset_password", data=data)
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
