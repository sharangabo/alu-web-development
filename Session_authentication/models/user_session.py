#!/usr/bin/env python3
from models import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey

class UserSession(BaseModel, Base):
    """
    UserSession model for storing user sessions in a database
    """
    __tablename__ = 'user_sessions'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    session_id = Column(String(60), nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Constructor for the UserSession model
        """
        super().__init__(*args, **kwargs)
