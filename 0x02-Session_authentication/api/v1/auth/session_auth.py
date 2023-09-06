#!/usr/bin/env python3
""" Defining authentication class """
from flask import request
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """SessionAuth class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """To create a session id for a user"""
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """this method returns a User ID based on a Session ID:"""
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        This method return a User instance based on a cookie value
        """
        # Get the session cookie value from the request
        session_cookie_value = self.session_cookie(request)

        # Use session_cookie_value to get the User ID
        user_id = self.user_id_for_session_id(session_cookie_value)

        if user_id:
            # Retrieve the User instance from the
            # + database based on the User ID
            user = User.get(user_id)
            return user
        else:
            return None

    def destroy_session(self, request=None):
        """deleteing the user session / logout"""
        if not request:
            return False

        # Check if the request does not have session id cookie
        session_cookie_val = self.session_cookie(request)
        if not session_cookie_val:
            return False

        # check if the session id is not linked to a user id
        user_id = self.user_id_for_session_id(session_cookie_val)
        if not user_id:
            return False

        # delete the session from 'the user_id_by_session_id'
        del self.user_id_by_session_id[session_cookie_val]

        return True
