#!/usr/bin/env python3
""" Handling session life span """
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """This class handles session expiration"""

    def __init__(self):
        super().__init__()

        # Read the SESSION_DURATION environment
        # + variable and set session_duration
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION", "0"))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """This method will customize the create_session method"""
        # Call the parent class method to create a Session ID
        session_id = super().create_session(user_id)

        if session_id:
            # Create a session dictionary with user_id and created_at
            session_dict = {"user_id": user_id, "created_at": datetime.now()}

            # Store the session dictionary in user_id_by_session_id
            self.user_id_by_session_id[session_id] = session_dict

            return session_id
        else:
            return None

    def user_id_for_session_id(self, session_id=None):
        """to return a user if the session is not expired"""
        if not session_id:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)

        if not session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")

        if not created_at:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if datetime.now() > expiration_time:
            return None

        return session_dict.get("user_id")
