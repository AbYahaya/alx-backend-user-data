#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
import logging
from user import Base, User
# Suppress SQLAlchemy info/debug logs
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        Args:
            email (str): The user's email
            hashed_password (str): The user's hashed password

        Returns:
            User: The newly created user object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user based on arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering.

        Raises:
            NoResultFound: If no user matches the filter criteria.
            InvalidRequestError: If invalid query arguments are provided.

        Returns:
            User: The user object that matches the filter criteria.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found with the specified criteria.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments provided.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Key-value pairs of attributes to update.

        Raises:
            ValueError: If an invalid attribute is passed.
        """
        user = self.find_user_by(id=user_id)  # Locate the user
        for key, value in kwargs.items():
            if not hasattr(user, key):  # Check if the attribute exists
                raise ValueError(f"{key} is not a valid attribute of User")
            setattr(user, key, value)  # Update the attribute dynamically
        self._session.commit()  # Commit changes to the database
