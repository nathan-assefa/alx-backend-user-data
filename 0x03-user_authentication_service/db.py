#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database
        """

        # Frist create a new user with the provided email and passowrd
        user = User(email=email, hashed_password=hashed_password)

        # Then add the user to the database
        self._session.add(user)

        # Then commite the change and close the session
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user based on keywords"""

        try:
            # let's first query a user based on the kwargs arguments
            query = self._session.query(User).filter_by(**kwargs)

            # Let's then find the first user instance from the resutl
            user = query.first()

            if not user:
                raise NoResultFound

            return user
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updating a specific user"""
        try:
            # Find the user to update using user_id
            user = self.find_user_by(id=user_id)

            for key, val in kwargs.items():
                setattr(user, key, val)

            # Commit the changes to the database
            self._session.commit()
        except (InvalidRequestError, NoResultFound, ValueError):
            # raise will handle the most recent exception
            raise
