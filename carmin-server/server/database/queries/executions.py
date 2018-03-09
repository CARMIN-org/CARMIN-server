from typing import List
from server.database.models.execution import Execution


def get_all_executions_for_user(username: str, db_session) -> List[Execution]:
    return list(
        db_session.query(Execution).filter(
            Execution.creator_username == username).order_by(
                Execution.created_at.desc()))


def get_execution(identifier: str, db_session) -> Execution:
    return db_session.query(Execution).filter_by(identifier=identifier).first()


def get_execution_count_for_user(username: str, db_session) -> int:
    return db_session.query(Execution).filter(
        Execution.creator_username == username).count()
