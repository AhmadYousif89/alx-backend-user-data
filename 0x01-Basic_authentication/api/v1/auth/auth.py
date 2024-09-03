#!/usr/bin/env python3
""" Module of Auth views
"""

from typing import List
from flask import request
from typing import TypeVar


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Helper function to check if a path requires authentication or not.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'  # add trailing slash
        if path in excluded_paths:
            return False  # do not require authentication
        return True  # require authentication

    def authorization_header(self, request=None) -> str:
        """
        Helper function to get the Authorization header from a request.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Helper function to get the current user.
        """
        return None
