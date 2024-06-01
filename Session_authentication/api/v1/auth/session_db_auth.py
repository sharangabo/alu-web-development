#!/usr/bin/env python3
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv

class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class for authentication with session ID stored in a database
    """
    def __init__(self):
        super().__init__()
        self.db_engine = create_engine(getenv('DB_URL'))
        self.db_session = sessionmaker(bind=self.db_engine)

    def create_session(self, user_id=None):
        """
        Creates a new session and stores it in the database
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session = self.db_session()
        user_session = UserSession(user_id=user_id, session_id=session_id)
        session.add(user_session)
        session.commit()
        session.close()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the user ID associated with the given session ID
        """
        if session_id is None:
            return None

        session = self.db_session()
        user_session = session.query(UserSession).filter_by(session_id=session_id).first()
        if user_session is None:
            return None

        user_id = user_session.user_id
        session.close()

        return self.user_id_for_session_id_in_memory(session_id, user_id)

    def destroy_session(self, request=None):
        """
        Destroys the session associated with the given request
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        session = self.db_session()
        user_session = session.query(UserSession).filter_by(session_id=session_id).first()
        if user_session is None:
            return False

        self.user_id_by_session_id.pop(session_id, None)
        session.delete(user_session)
        session.commit()
        session.close()

        return True
