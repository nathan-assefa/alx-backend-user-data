#!/usr/bin/env python3
""" Defining authentication class """
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        to perform authentication checks based on the given
        path and excluded_paths
        """
        if not path:
            return True
        if not excluded_paths:
            return True

        path = path.rstrip("/")

        for excluded_path in excluded_paths:
            if excluded_path.endswith("*"):
                # Remove the '*' character and check if the path
                # +starts with the remaining part
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path.rstrip("/"):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        to extract the authorization header from the Flask
        request object.
        """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar("User"):
        """
        to retrieve information about the current user
        """
        return None

    def session_cookie(self, request=None):
        """This method returns a cookie value from a request"""
        import os

        if not request:
            return None
        # Get the session cookie name from the SESSION_NAME
        # + environment variable
        session_cookie_name = os.environ.get("SESSION_NAME")

        # Use .get() to access the cookie value from the
        # + request cookies dictionary
        return request.cookies.get(session_cookie_name)
