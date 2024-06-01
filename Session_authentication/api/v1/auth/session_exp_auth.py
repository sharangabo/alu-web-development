#!/usr/bin/env python3

"""
Module for Session Authentication with expiration
"""

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta

class SessionExpAuth(SessionAuth):
    def __init__(self):
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dict.get('user_id')

        if 'created_at' not in session_dict:
            return None

        created_at = session_dict.get('created_at')
        if created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return session_dict.get('user_id')
