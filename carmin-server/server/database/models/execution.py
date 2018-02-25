import enum
import uuid
from flask_restful import fields
from sqlalchemy import Column, String, Enum, Integer
from server import db
from server.resources.models.execution import ExecutionStatus


class Execution(db.Model):
    """Execution

    Args:
        identifier (str):
        name (str):
        pipeline_identifier (Role):
        timeout (int):
        status (ExecutionStatus):
        study_identifier (str):
        error_code (int):
        start_date (int):
        end_date (int):

    Attributes:
        identifier (str):
        name (str):
        pipeline_identifier (Role):
        timeout (int):
        status (ExecutionStatus):
        study_identifier (str):
        error_code (int):
        start_date (int):
        end_date (int):
    """

    identifier = Column(String, primary_key=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    pipeline_identifier = Column(String, nullable=False)
    timeout = Column(Integer)
    status = Column(Enum(ExecutionStatus), nullable=False)
    study_identifier = Column(String)
    error_code = Column(Integer)
    start_date = Column(Integer)
    end_date = Column(Integer)
