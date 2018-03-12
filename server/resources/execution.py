from flask_restful import Resource
from server.database.queries.executions import get_execution
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageFormatter, EXECUTION_NOT_FOUND, INVALID_MODEL_PROVIDED,
    CANNOT_MODIFY_PARAMETER)
from server.resources.models.execution import ExecutionSchema
from server.resources.helpers.executions import get_execution_as_model
from server.resources.decorators import (login_required, get_db_session,
                                         marshal_response, unmarshal_request)


class Execution(Resource):
    @login_required
    @get_db_session
    @marshal_response(ExecutionSchema())
    def get(self, user, db_session, execution_identifier):
        execution_db = get_execution(execution_identifier, db_session)
        execution, error = get_execution_as_model(user.username, execution_db)
        if error:
            return ErrorCodeAndMessageFormatter(EXECUTION_NOT_FOUND,
                                                execution_identifier)
        return execution

    @login_required
    @get_db_session
    @unmarshal_request(ExecutionSchema(), partial=True)
    @marshal_response()
    def put(self, model, execution_identifier, user, db_session):
        if model.identifier:
            return ErrorCodeAndMessageFormatter(CANNOT_MODIFY_PARAMETER,
                                                "identifier")
        if model.status:
            return ErrorCodeAndMessageFormatter(CANNOT_MODIFY_PARAMETER,
                                                "status")

        if model.name or model.timeout:
            execution_db = get_execution(execution_identifier, db_session)
            if not execution_db:
                return ErrorCodeAndMessageFormatter(EXECUTION_NOT_FOUND,
                                                    execution_identifier)
            if model.name:
                execution_db.name = model.name
            if model.timeout:
                execution_db.timeout = model.timeout
            db_session.add(execution_db)
            db_session.commit()

    def delete(self, execution_identifier):
        pass
