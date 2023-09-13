#!/usr/bin/env python3
"""DB module
"""
import bcrypt
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from uuid import uuid4
from typing import Union


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

    def get_user_from_session_id(self, session_id: str) -> Union[user, None]:
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=sesssion_id)
            return user
        except NoResultFound:
            return None