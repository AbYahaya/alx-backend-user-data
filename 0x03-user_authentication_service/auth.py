#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt

def _hash_password(password: str) -> bytes:
    """Hashes a password with bcrypt and returns the salted hash.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hash the password
    return hashed_password
