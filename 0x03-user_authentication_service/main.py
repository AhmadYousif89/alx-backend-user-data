#!/usr/bin/env python3
"""
End-to-end integration test 
"""
from db import DB
from user import User
from auth import Auth

AUTH = Auth()
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str):
    """Register a user"""
    AUTH.register_user(email, password)


def log_in_wrong_password(email: str, password: str):
    """Log in with wrong password"""
    assert AUTH.valid_login(email, password) is False


def log_in(email: str, password: str) -> str:
    """Log in"""
    session_id = AUTH.create_session(email)
    assert session_id is not None
    return session_id


def profile_unlogged():
    """Profile of an unlogged user"""
    user = AUTH.get_user_from_session_id(None)
    assert user is None
    user = AUTH.get_user_from_session_id('')
    assert user is None
    user = AUTH.get_user_from_session_id('invalid sid')
    assert user is None


def profile_logged(session_id: str):
    """Profile of a logged user"""
    user = AUTH.get_user_from_session_id(session_id)
    assert user is not None
    assert isinstance(user, User)
    assert isinstance(user.email, str)
    assert user.email == EMAIL


def log_out(session_id: str):
    """Log out"""
    user = AUTH.get_user_from_session_id(session_id)
    assert user is not None
    user_id = user.id
    assert isinstance(user_id, int), "user.id must be an integer"
    AUTH.destroy_session(user_id)
    user = AUTH.get_user_from_session_id(session_id)
    assert user is None


def reset_password_token(email: str) -> str:
    """Reset password token"""
    token = AUTH.get_reset_password_token(email)
    assert token is not None
    return token


def update_password(email: str, reset_token: str, new_password: str):
    """Update password"""
    AUTH.update_password(reset_token, new_password)
    assert AUTH.valid_login(email, PASSWD) is False
    assert AUTH.valid_login(email, new_password) is True


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
