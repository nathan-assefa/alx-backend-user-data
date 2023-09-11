#!/usr/bin/env python3
"""DB module
"""
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ takes in string and return bytes """
    salt = bcrypt.gensalt()

    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hash_password


from db import DB


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register a new user """

        try:
            # Attempt to find a user with the same email
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If no user with the same email is found,
            # + proceed to register
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
