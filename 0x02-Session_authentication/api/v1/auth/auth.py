#!/usr/bin/env python3
""" Authentication module for the API
"""

from typing import List, TypeVar
from os import getenv


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if the given request path is not in the list of
        excluded paths and returns False if it is, and True if it is not.
        """
        if not path or not excluded_paths:
            return True
        normalized_path = path.rstrip('/')

        for excluded_path in excluded_paths:
            normalized_excluded_path = excluded_path.rstrip('/')
            if normalized_excluded_path.endswith('*'):
                if normalized_path.startswith(normalized_excluded_path[:-1]):
                    return False
            elif normalized_path == normalized_excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Returns the value of the Authorization header from a request"""
        if request is None or request.headers.get('Authorization') is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """public method"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None

        SESSION_NAME = getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(SESSION_NAME)
