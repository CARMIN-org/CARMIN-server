import enum
from flask_restful import fields
from sqlalchemy import Column, String, Enum
from server import db


class Role(enum.Enum):
    admin = 1
    user = 2


class User(db.Model):
    """User

    Args:
        username (str):
        password (str):
        role (Role):
        api_key (str):

    Attributes:
        username (str):
        password (str):
        role (Role):        
        api_key (str):
    """

    username = Column(String, primary_key=True)
    password = Column(String)
    role = Column(Enum(Role))
    api_key = Column(String, unique=True)
