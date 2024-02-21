#!/usr/bin/env python3
"""
DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import User

Base = declarative_base()

class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """
        Add a new user to the database.

        Parameters:
        - email (str): The email of the user.
        - hashed_password (str): The hashed password of the user.

        Returns:
        - User: The User object representing the newly added user.
        """

        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        try:
            self._session.commit()
        except IntegrityError:
            # Handle integrity error if necessary
            self._session.rollback()
            raise Exception("User already exists with email {}".format(email))
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by specified criteria.

        Parameters:
        - **kwargs: Arbitrary keyword arguments representing filtering criteria.

        Returns:
        - User: The User object representing the found user.

        Raises:
        - NoResultFound: If no user is found matching the given criteria.
        - InvalidRequestError: If wrong query arguments are passed.
        """

        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except InvalidRequestError as e:
            self._session.rollback()
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes.

        Parameters:
        - user_id (int): The id of the user to update.
        - **kwargs: Arbitrary keyword arguments representing attributes to update.

        Returns:
        - None

        Raises:
        - ValueError: If an argument that does not correspond to a user attribute is passed.
        """

        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(User, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(f"Invalid attribute: {key}")
            self._session.commit()
        except NoResultFound:
            raise ValueError(f"User not found with id {user_id}")
