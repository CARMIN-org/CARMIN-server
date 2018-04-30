from flask_restful import Resource, request, inputs
from server.database import db
from server.database.models.execution import ExecutionStatus, current_milli_time
from server.database.queries.executions import get_execution, get_execution_processes
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageFormatter, EXECUTION_NOT_FOUND, CANNOT_MODIFY_PARAMETER,
    UNAUTHORIZED, CANNOT_KILL_FINISHING_EXECUTION,
    CANNOT_KILL_NOT_RUNNING_EXECUTION)
from server.resources.models.execution import ExecutionSchema, EXECUTION_COMPLETED_STATUSES
from server.resources.helpers.executions import (
    get_execution_as_model, get_execution_dir, delete_execution_directory)
from server.resources.helpers.execution_kill import kill_all_execution_processes
from server.resources.decorators import (login_required, marshal_response,
                                         unmarshal_request)


class Execution(Resource):
    @login_required
    @marshal_response(ExecutionSchema())
    def get(self, user, execution_identifier):
        execution_db = get_execution(execution_identifier, db.session)
        execution, error = get_execution_as_model(user.username, execution_db)
        if error:
            return ErrorCodeAndMessageFormatter(EXECUTION_NOT_FOUND,
                                                execution_identifier)
        return execution

    @login_required
    @unmarshal_request(ExecutionSchema(), partial=True)
    @marshal_response()
    def put(self, model, execution_identifier, user):
        if model.identifier:
            return ErrorCodeAndMessageFormatter(CANNOT_MODIFY_PARAMETER,
                                                "identifier")
        if model.status:
            return ErrorCodeAndMessageFormatter(CANNOT_MODIFY_PARAMETER,
                                                "status")

        if model.name or model.timeout:
            execution_db = get_execution(execution_identifier, db.session)
            if not execution_db:
                return ErrorCodeAndMessageFormatter(EXECUTION_NOT_FOUND,
                                                    execution_identifier)
            if model.name:
                execution_db.name = model.name
            if model.timeout:
                execution_db.timeout = model.timeout
            db.session.add(execution_db)
            db.session.commit()

    @login_required
    @marshal_response()
    def delete(self, user, execution_identifier):
        execution_db = get_execution(execution_identifier, db.session)
        if not execution_db:
            return ErrorCodeAndMessageFormatter(EXECUTION_NOT_FOUND,
                                                execution_identifier)
        if execution_db.creator_username != user.username:
            return UNAUTHORIZED

        deleteFiles = request.args.get(
            'deleteFiles', default=False, type=inputs.boolean)

        # Get all the execution running processes
        execution_processes = get_execution_processes(execution_identifier,
                                                      db.session)

        # Given delete is called to perform only a kill and encounter the same situation as kill, we do not kill the processes
        # See execution_kill for more information
        if execution_db.status == ExecutionStatus.Running and not execution_processes and not deleteFiles:
            return CANNOT_KILL_FINISHING_EXECUTION

        if execution_db.status != ExecutionStatus.Running and not deleteFiles:
            return ErrorCodeAndMessageFormatter(
                CANNOT_KILL_NOT_RUNNING_EXECUTION, execution_db.status.name)

        # Kill all the execution processed
        kill_all_execution_processes(execution_processes)
        for execution_process in execution_processes:
            db.session.delete(execution_process)
        # If the execution is not in a completed status, we mark it as killed
        if execution_db.status == ExecutionStatus.Running:
            execution_db.status = ExecutionStatus.Killed
            execution_db.end_date = current_milli_time()
        db.session.commit()

        # Free all resources associated with the execution if delete files is True
        if deleteFiles:
            execution_dir = get_execution_dir(user.username,
                                              execution_identifier)
            delete_execution_directory(execution_dir)
            db.session.delete(execution_db)
            db.session.commit()
