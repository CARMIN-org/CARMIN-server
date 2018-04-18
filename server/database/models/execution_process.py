from flask_restful import fields
from sqlalchemy import Column, String, Integer, ForeignKey
from server.database import db


class ExecutionProcess(db.Model):
    """ExecutionProcess

    Args:
        execution_identifier (str):
        pid (int):

    Attributes:
        execution_identifier (str):
        pid (int):
    """

    execution_identifier = Column(
        String, ForeignKey("execution.identifier"), primary_key=True)
    pid = Column(Integer, nullable=False)
