#!/usr/bin/env python3
"""
Basic Authentication module for the API
"""

import base64
from flask import request
from typing import List, TypeVar
from models.user import User


class BasicAuth:
    """
    BasicAuth class for managing Basic Authentication
    """

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header

        Args:
            request: The Flask request object.

        Returns:
            str: The authorization header.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for the given path

        Args:
            path (str): The path to check for authentication requirement.
            excluded_paths (List[str]): A list of paths that are excluded
            from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Normalize paths by ensuring they end with '/'
        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            if path == excluded_path:
                return False

        return True

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'): The current user.
        """
        authorization_header = self.authorization_header(request)
        if not authorization_header:
            return None

        base64_header = self.extract_base64_authorization_header(
                authorization_header)
        if not base64_header:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)
        if not decoded_header:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        if not user_email or not user_pwd:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic
        Authentication

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            str: The Base64 part of the Authorization header, or None if not
            found.
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 string

        Args:
            base64_authorization_header (str): The Base64 string to decode.

        Returns:
            str: The decoded value as UTF-8 string, or None if decoding fails.
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user credentials from the decoded Base64 authorization header

        Args:
            decoded_base64_authorization_header (str): The decoded Base64
            authorization header.

        Returns:
            (str, str): A tuple containing user email and password, or
            (None, None) if not found.
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None

        credentials = decoded_base64_authorization_header.split(':', 1)
        if len(credentials) != 2:
            return None, None

        email = credentials[0]
        password = credentials[1]
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieves the User instance based on email and password

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            TypeVar('User'): The User instance, or None if not found or
            password is incorrect.
        """
        if user_email is None or not isinstance(user_email, str) or \
           user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user
