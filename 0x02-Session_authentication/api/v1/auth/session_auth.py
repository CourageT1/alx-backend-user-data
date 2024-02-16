#!/usr/bin/env python3
"""
Session Authentication module for the API
"""
from typing import Optional
from api.v1.auth.auth import Auth
from flask import request


class SessionAuth(Auth):
    """
    SessionAuth class for managing API session authentication
    """

    def __init__(self):
        """
        Constructor
        """
        self.session_cookie_name = request.environ.get(
                'SESSION_NAME', '_my_session_id')
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> Optional[str]:
        """
        Creates a session ID for a user ID

        Args:
            user_id (str): The user ID.

        Returns:
            str: The session ID.
        """
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> Optional[str]:
        """
        Retrieves a user ID based on a session ID

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID.
        """
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves the current user based on the session ID

        Args:
            request: The Flask request object.

        Returns:
            User: The current user.
        """
        session_id = self.session_cookie(request)
        if session_id:
            user_id = self.user_id_for_session_id(session_id)
            if user_id:
                return User.get(user_id)
        return None

    def destroy_session(self, request=None) -> bool:
        """
        Deletes the user session / logout

        Args:
            request: The Flask request object.

        Returns:
            bool: True if the session was successfully destroyed, False
            otherwise.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True
        return False
