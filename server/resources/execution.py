from flask_restful import Resource
from server.database import db
from server.database.queries.executions import get_execution
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageFormatter, EXECUTION_NOT_FOUND, CANNOT_MODIFY_PARAMETER)
from server.resources.models.execution import ExecutionSchema
from server.resources.helpers.executions import get_execution_as_model
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

    def delete(self, execution_identifier):
        pass
