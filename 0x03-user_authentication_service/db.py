#!/usr/bin/env python3
""" SQLAlchemy DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import TypeVar
from user import Base, User

DATA_FIELDS = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    """
    DB class.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """
        private property.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        METHOD that save the user to the database.
        """
        if not email or not hashed_password:
            return
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        METHOD to locate the user to update.
        """
        if not kwargs or any(x not in DATA_FIELDS for x in kwargs):
            raise InvalidRequestError
        session = self._session
        try:
            return session.query(User).filter_by(**kwargs).one()
        except Exception:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        METHOD to update users.
        """
        session = self._session
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if k not in DATA_FIELDS:
                raise ValueError
            setattr(user, k, v)
        session.commit()
