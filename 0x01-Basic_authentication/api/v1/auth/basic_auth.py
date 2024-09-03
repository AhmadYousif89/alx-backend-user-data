#!/usr/bin/env python3
""" Basic Authentication module for the API
"""

from api.v1.auth.auth import Auth
from models.user import User
from typing import Tuple
import base64


class BasicAuth(Auth):
    """Basic Authentication class"""

    # def extract_base64_authorization_header(
    #     self, authorization_header: str
    # ) -> str:
    #     """Extracts and returns the Base64 part of the Authorization header."""
    #     if (
    #         authorization_header is None
    #         or type(authorization_header) is not str
    #         or not authorization_header.startswith('Basic ')
    #     ):
    #         return None

    #     return authorization_header[6:]

    # def decode_base64_authorization_header(
    #     self, base64_authorization_header: str
    # ) -> str:
    #     """Decodes a Base64-encoded string, returning the decoded string."""
    #     if (
    #         base64_authorization_header is None
    #         or type(base64_authorization_header) is not str
    #     ):
    #         return None

    #     try:
    #         decoded_bytes = base64.b64decode(
    #             base64_authorization_header, validate=True
    #         )
    #         return decoded_bytes.decode('utf-8')
    #     except Exception:
    #         return None

    # def extract_user_credentials(
    #     self, decoded_base64_authorization_header: str
    # ) -> Tuple[str, str]:
    #     """
    #     Extracts and returns the user email and password from the
    #     decoded Base64 Authorization header.
    #     """
    #     if (
    #         decoded_base64_authorization_header is None
    #         or type(decoded_base64_authorization_header) is not str
    #         or ':' not in decoded_base64_authorization_header
    #     ):
    #         return None, None

    #     email, password = decoded_base64_authorization_header.split(':', 1)
    #     return email, password

    # def user_object_from_credentials(
    #     self, user_email: str, user_pwd: str
    # ) -> TypeVar('User'):
    #     """Returns the User instance based on his email and password."""
    #     if (
    #         user_email is None
    #         or user_pwd is None
    #         or type(user_email) is not str
    #         or type(user_pwd) is not str
    #     ):
    #         return None

    #     try:
    #         user = User.search({'email': user_email})[0]
    #         if user is None or not user.is_valid_password(user_pwd):
    #             return None
    #         return user
    #     except Exception:
    #         return None

    # def current_user(self, request=None) -> TypeVar('User'):
    #     """Overloads Auth and retrieves the User instance for a request."""
    #     auth_header = self.authorization_header(request)
    #     base64_header = self.extract_base64_authorization_header(auth_header)
    #     decoded_header = self.decode_base64_authorization_header(base64_header)
    #     email, password = self.extract_user_credentials(decoded_header)
    #     return self.user_object_from_credentials(email, password)
