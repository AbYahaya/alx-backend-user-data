#!/usr/bin/env python3
"""
Auth module
"""
from db import DB
from user import User
from bcrypt import hashpw, gensalt
from sqlalchemy.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    """Hash a password with bcrypt."""
    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the given email and password.

        Args:
            email (str): User's email.
            password (str): User's password.

        Raises:
            ValueError: If a user with the given email already exists.

        Returns:
            User: The newly created User object.
        """
        try:
            # Check if user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If user does not exist, create a new one
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(
                email=email,
                hashed_password=hashed_password.decode('utf-8'),
            )
            return new_user
