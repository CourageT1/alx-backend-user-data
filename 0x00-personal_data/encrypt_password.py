#!/usr/bin/env python3
"""
Module: encrypt_password
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash the given password using bcrypt.

    Arguments:
    password: str representing the password to be hashed

    Returns:
    bytes: salted, hashed password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if the provided password matches the hashed password.

    Arguments:
    hashed_password: bytes representing the hashed password
    password: str representing the password to be validated

    Returns:
    bool: True if the password matches the hashed password, False otherwise
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
