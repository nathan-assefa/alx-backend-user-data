#!/usr/bin/env python3
""" Bsic authentication """


from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Definig basic auths"""

    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        '''
        Extract the Base64 part of the Authorization header
        for Basic Authentication.
        '''
        if not authorization_header:
            return None
        if type(authorization_header) != str:
            return None
        if authorization_header.split()[0] != 'Basic':
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        '''
        Decode the Base64 authorization header and return
        the decoded value as a UTF-8 string.
        '''
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        '''
        Extract user email and password from the Base64
        decoded authorization header.
        '''
        decoded_base64 = decoded_base64_authorization_header
        is_str = isinstance(decoded_base64_authorization_header, str)
        if not decoded_base64 or not is_str:
            return None, None

        # Split the decoded header into email and password using ':'
        credentials = decoded_base64_authorization_header.split(':')

        if len(credentials) != 2:
            return None, None

        user_email, user_password = credentials
        return user_email, user_password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        '''
        Retrieve a User instance based on email and password.
        '''
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Lookup users by email from your database (file)
        users = User.search({'email': user_email})

        # Check if there are any users with the provided email
        if not users:
            return None

        # Check if the provided password matches the user's password
        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None
