#!/usr/bin/env python3
"""
providing session-based authentication with database
storage for user sessions in a Flask application
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """session-bases authentication with database"""

    def create_session(self, user_id=None):
        """
        Create and store a new instance of UserSession and
        return the Session ID.
        """
        if user_id:
            session_id = super().create_session(user_id)

            if session_id:
                # Create and store a new UserSession instance in the database
                new_session = UserSession(
                        session_id=session_id, user_id=user_id
                        )

                # Implement the save() method in UserSession model
                new_session.save()

                return session_id

        return None

    def user_id_for_session_id(self, session_id=None):
        """
        Return the User ID by querying UserSession in the
        database based on session_id.
        """
        if session_id:
            # Query the UserSession instance from
            # + the database based on session_id
            user_session = UserSession.get(session_id)

            if user_session:
                return user_session.user_id

        return None

    def destroy_session(self, request=None):
        """
        Destroy the UserSession based on the Session
        ID from the request cookie.
        """
        if request:
            session_id = self.session_cookie(request)

            if session_id:
                # Query and delete the UserSession instance from the database
                user_session = UserSession.get(session_id)

                if user_session:
                    user_session.delete()
                    return True

        return False
