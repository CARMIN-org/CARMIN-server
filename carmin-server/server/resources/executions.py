from flask_restful import Resource, request
from sqlalchemy.exc import IntegrityError
from server.database.models.execution import Execution, ExecutionStatus
from server.common.error_codes_and_messages import (
    EXECUTION_IDENTIFIER_MUST_NOT_BE_SET, INVALID_INPUT_FILE, UNEXPECTED_ERROR,
    INVALID_QUERY_PARAMETER, ErrorCodeAndMessageFormatter,
    ErrorCodeAndMessageMarshaller)
from server.resources.helpers.executions import (
    write_inputs_to_file, create_execution_directory, get_execution_as_model,
    input_files_exist, validate_request_model, filter_executions)
from server.database.queries.executions import (get_all_executions_for_user,
                                                get_execution)
from .models.execution import ExecutionSchema
from .decorators import unmarshal_request, marshal_response, login_required, get_db_session


class Executions(Resource):
    @login_required
    @get_db_session
    @marshal_response(ExecutionSchema(many=True))
    def get(self, user, db_session):
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        user_executions = get_all_executions_for_user(user.username,
                                                      db_session)
        for i, execution in enumerate(user_executions):
            exe, error = get_execution_as_model(user.username, execution)
            if error:
                return error
            user_executions[i] = exe

        user_executions, error = filter_executions(user_executions, offset,
                                                   limit)
        if error:
            return error

        return user_executions

    @login_required
    @get_db_session
    @unmarshal_request(ExecutionSchema())
    @marshal_response(ExecutionSchema())
    def post(self, model, user, db_session):
        _, error = validate_request_model(model, request.url_root)
        if error:
            return error

        try:
            new_execution = Execution(
                name=model.name,
                pipeline_identifier=model.pipeline_identifier,
                timeout=model.timeout,
                status=ExecutionStatus.Initializing,
                study_identifier=model.study_identifier,
                creator_username=user.username)
            db_session.add(new_execution)
            db_session.commit()

            path, error = create_execution_directory(new_execution, user)
            if error:
                db_session.rollback()
                return error

            error = write_inputs_to_file(model, path)
            if error:
                db_session.rollback()
                return error

            execution_db = get_execution(new_execution.identifier, db_session)
            if not execution_db:
                return UNEXPECTED_ERROR
            execution, error = get_execution_as_model(user.username,
                                                      execution_db)
            if error:
                return UNEXPECTED_ERROR
            return execution
        except IntegrityError:
            db_session.rollback()
