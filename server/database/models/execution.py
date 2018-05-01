import enum
import uuid
import time
from flask_restful import fields
from sqlalchemy import Column, String, Enum, Integer, BigInteger, ForeignKey
from server.database import db
from server.resources.models.execution import ExecutionStatus


def execution_uuid() -> str:
    return str(uuid.uuid4())


current_milli_time = lambda: int(round(time.time() * 1000))


class Execution(db.Model):
    """Execution

    Args:
        identifier (str):
        name (str):
        pipeline_identifier (str):
        descriptor (str):
        timeout (int):
        status (ExecutionStatus):
        study_identifier (str):
        error_code (int):
        start_date (int):
        end_date (int):
        creator_username (str):

    Attributes:
        identifier (str):
        name (str):
        pipeline_identifier (str):
        descriptor (str):
        timeout (int):
        status (ExecutionStatus):
        study_identifier (str):
        error_code (int):
        start_date (int):
        end_date (int):
        creator_username (str):
    """

    identifier = Column(String, primary_key=True, default=execution_uuid)
    name = Column(String, nullable=False)
    pipeline_identifier = Column(String, nullable=False)
    descriptor = Column(String, nullable=False)
    timeout = Column(Integer)
    status = Column(Enum(ExecutionStatus), nullable=False)
    study_identifier = Column(String)
    error_code = Column(Integer)
    start_date = Column(BigInteger)
    end_date = Column(BigInteger)
    creator_username = Column(
        String, ForeignKey("user.username"), nullable=False)
    created_at = Column(BigInteger, default=current_milli_time)
    last_update = Column(BigInteger, onupdate=current_milli_time)
