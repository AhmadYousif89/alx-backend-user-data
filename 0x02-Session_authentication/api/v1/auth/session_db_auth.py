#!/usr/bin/env python3
"""
Session DB Authentication Module
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""

    def create_session(self, user_id: str = None):
        """Create session"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {'user_id': user_id, 'session_id': session_id}
        UserSession(**session_dict).save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return user ID based on session ID"""
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})[0]
        if (
            not user_session
            or (datetime.utcnow() - user_session.created_at).seconds
            > self.session_duration
        ):
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user = UserSession.search({'session_id': session_id})[0]
        if not user:
            return False
        user.remove()
        return True
