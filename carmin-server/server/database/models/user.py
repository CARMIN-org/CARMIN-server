from flask_restful import fields
from sqlalchemy import Column, String
from server import db


class User(db.Model):
    """User

    Args:
        username (str):
        password (str):
        api_key

    Attributes:
        username (str):
        password (str):
        api_key (str):
    """

    username = Column(String, primary_key=True)
    password = Column(String)
    api_key = Column(String, unique=True)
