#!/usr/bin/env python3
"""
Session DB Authentication Module
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""

    def create_session(self, user_id: str = None):
        """Create session"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {'user_id': user_id, 'created_at': datetime.now()}
        UserSession(**session_dict).save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return user ID based on session ID"""
        if session_id is None:
            return None
        user = UserSession.search({'session_id': session_id})[0]
        if not user:
            return None
        if self.session_duration <= 0:
            return user.user_id
        if 'created_at' not in user:
            return None
        created_at = user.get('created_at')
        if (datetime.now() - created_at).seconds > self.session_duration:
            return None
        return user.user_id

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
        try:
            user.remove()
            UserSession.save_to_file()
        except Exception:
            return False
        return True
