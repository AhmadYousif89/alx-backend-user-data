#!/usr/bin/env python3
"""DB module
"""
from typing import Union
from sqlalchemy import Column, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base

from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db")
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
        """Add a new user to the database"""
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by a given keyword argument"""
        from sqlalchemy.exc import InvalidRequestError
        from sqlalchemy.orm.exc import NoResultFound  # type: ignore

        try:
            result = self._session.query(User).filter_by(**kwargs).first()
            if result is None:
                raise NoResultFound
        except InvalidRequestError:
            raise
        return result

    def update_user(self, user_id: Union[Column[int], int], **kwargs) -> None:
        """Update a user by its id"""
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            user.__setattr__(key, value)
        self._session.commit()
