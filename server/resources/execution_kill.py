from flask_restful import Resource
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageFormatter, ErrorCodeAndMessageAdditionalDetails,
    EXECUTION_NOT_FOUND, UNAUTHORIZED, UNEXPECTED_ERROR,
    CANNOT_KILL_NOT_RUNNING_EXECUTION, CANNOT_KILL_FINISHING_EXECUTION)
from server.database import db
from server.database.queries.executions import get_execution, get_execution_processes
from server.database.models.execution import Execution, ExecutionStatus, current_milli_time
from server.resources.decorators import login_required, marshal_response
from server.resources.helpers.execution_kill import kill_all_execution_processes


class ExecutionKill(Resource):
    @login_required
    @marshal_response()
    def put(self, user, execution_identifier):
        execution_db = get_execution(execution_identifier, db.session)
        if not execution_db:
            return ErrorCodeAndMessageFormatter(EXECUTION_NOT_FOUND,
                                                execution_identifier)
        if user.role != Role.admin and execution_db.creator_username != user.username:
            return UNAUTHORIZED

        if execution_db.status != ExecutionStatus.Running:
            return ErrorCodeAndMessageFormatter(
                CANNOT_KILL_NOT_RUNNING_EXECUTION, execution_db.status.name)

        # Look at its running processes
        execution_processes = get_execution_processes(execution_identifier,
                                                      db.session)

        if not execution_processes:  # Most probably due to the execution being in termination process
            return CANNOT_KILL_FINISHING_EXECUTION

        kill_all_execution_processes(execution_processes)

        # Mark the execution as "Killed" and delete the execution processes
        execution_db.status = ExecutionStatus.Killed
        execution_db.end_date = current_milli_time()
        for execution_process in execution_processes:
            db.session.delete(execution_process)
        db.session.commit()
