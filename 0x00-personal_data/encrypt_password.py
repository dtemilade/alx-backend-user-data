#!/usr/bin/env python3
"""
Script to make User passwords NEVER be stored in plain text in a database.
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    hash password for security purpose
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ method to validate password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
