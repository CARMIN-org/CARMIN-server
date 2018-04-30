from typing import List
from server.database.models.execution import Execution
from server.database.models.execution_process import ExecutionProcess


def get_all_executions_for_user(username: str, limit: int, offset: int,
                                db_session) -> List[Execution]:
    return list(
        db_session.query(Execution).filter(
            Execution.creator_username == username).order_by(
                Execution.created_at.desc()).offset(offset).limit(limit))


def get_execution(identifier: str, db_session) -> Execution:
    return db_session.query(Execution).filter_by(identifier=identifier).first()


def get_execution_count_for_user(username: str, db_session) -> int:
    return db_session.query(Execution).filter(
        Execution.creator_username == username).count()


def get_execution_processes(execution_identifier: str,
                            db_session) -> List[ExecutionProcess]:
    return db_session.query(ExecutionProcess).filter(
        ExecutionProcess.execution_identifier == execution_identifier).all()
