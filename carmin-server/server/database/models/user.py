from flask_restful import fields
from sqlalchemy import Column, String
from server import db


class User(db.Model):
    """User

    Args:
        username (str):
        password (str):
        api_token

    Attributes:
        username (str):
        password (str):
        api_token (str):
    """

    username = Column(String, primary_key=True)
    password = Column(String)
    api_token = Column(String, unique=True)

    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password
