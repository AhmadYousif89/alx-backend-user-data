#!/usr/bin/env python3
"""
Auth module
"""

import bcrypt
from typing import Union
from db import DB, User


def _hash_password(password: str) -> bytes:
    """Takes in a password string arguments and returns bytes"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a UUID"""
    import uuid

    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def get_users(self):
        """Get all users"""
        return self._db.find_all(User)

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        from sqlalchemy.orm.exc import NoResultFound  # type: ignore

        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password.decode())
        raise RuntimeError("Unexpected condition in register_user")

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode(), user.hashed_password.encode()
            )
        except Exception:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """Create a session ID"""
        try:
            user = self._db.find_user_by(email=email)
            assert isinstance(user.id, int), "user.id must be an integer"
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            pass

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get user from session ID"""
        from sqlalchemy.orm.exc import NoResultFound  # type: ignore

        if not session_id:
            return
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return

    def destroy_session(self, user_id: int) -> None:
        """Destroy a user session ID"""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Get reset password token"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            assert isinstance(user.id, int), "user.id must be an integer"
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str):
        """Update user password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashpass = _hash_password(password)
            assert isinstance(user.id, int), "user.id must be an integer"
            self._db.update_user(user.id, hashed_password=hashpass.decode())
            self._db.update_user(user.id, reset_token=None)
        except Exception:
            raise ValueError
