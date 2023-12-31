#!/usr/bin/env python3
"""DB module
"""
import bcrypt
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


from db import DB
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """takes in string and return bytes"""
    salt = bcrypt.gensalt()

    hash_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    return hash_password


def _generate_uuid() -> str:
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a new user"""

        try:
            # Attempt to find a user with the same email
            self._db.find_user_by(email=email)
        except NoResultFound:
            # If no user with the same email is found,
            # + proceed to register
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """validating a user"""
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)
            hashed_password = password.encode("utf-8")

            return bcrypt.checkpw(hashed_password, user.hashed_password)

        except NoResultFound:
            pass

        return False

    def create_session(self, email: str) -> str:
        """creating a session for a user"""
        try:
            user = self._db.find_user_by(email=email)

            # create a session id
            session_id = _generate_uuid()

            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except (InvalidRequestError, NoResultFound, ValueError):
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ Finding a user via session_id """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Removing session from the user object """
        try:
            self._db.update_user(user_id, session_id=None)
        except (InvalidRequestError, NoResultFound, ValueError):
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ reseting user's password """
        try:
            user = self._db.find_user_by(email=email)

            # Generate a new UUID
            reset_token = _generate_uuid()

            # Update the user's session_id field
            self._db.update_user(user.id, reset_token=reset_token)

            return reset_token
        except NoResultFound:
            raise ValueError
    
    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)

            # Get a new hashed password
            new_hashed_password = _hash_password(password)

            # Replace the old password with the new hashed pssword
            self._db.update_user(
                    user.id, hashed_password=new_hashed_password, reset_token=None
                    )
        except NoResultFound:
            raise ValueError
