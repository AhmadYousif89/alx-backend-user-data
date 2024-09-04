#!/usr/bin/env python3
""" Module of Session in Database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Session in database Class"""

    def create_session(self, user_id=None):
        """Creation session database"""
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        kwargs = {'user_id': user_id, 'session_id': session_id}
        user_session = UserSession(**kwargs)
        user_session.save()
        UserSession.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """User ID for Session ID Database"""
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
        """Remove Session from Database"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        user_session = UserSession.search({'session_id': session_id})[0]
        if not user_session:
            return False

        try:
            user_session.remove()
        except Exception:
            return False

        return True
