#!/usr/bin/env python3
''' Encrypting password '''


import bcrypt


def hash_password(password: str) -> bytes:
    ''' Encrypting password '''
    # Generate a salt using gensalt method
    salt = bcrypt.gensalt()

    # Hash the password using the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password
