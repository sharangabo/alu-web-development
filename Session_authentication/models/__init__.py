#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv

DB_URL = getenv('DB_URL')

engine = create_engine(DB_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()

from models.user import User
from models.user_session import UserSession

Base.metadata.create_all(engine)
