#!/usr/bin/env python3
"""
Authentication module for the API
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """
    Auth class for managing API authentication
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
            from authentication. The paths in this list can contain "*" as
            a wildcard to match any characters.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Normalize paths by ensuring they end with '/'
        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*') and path.startswith(
                    excluded_path[:-1]):
                return False
            elif path == excluded_path:
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
        return None
