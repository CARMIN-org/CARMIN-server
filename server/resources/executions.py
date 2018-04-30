import logging
from flask_restful import Resource, request
from sqlalchemy.exc import IntegrityError
from server.database import db
from server.database.models.execution import Execution, ExecutionStatus
from server.platform_properties import PLATFORM_PROPERTIES
from server.common.error_codes_and_messages import UNEXPECTED_ERROR, INVOCATION_INITIALIZATION_FAILED
from server.resources.helpers.pipelines import (
    get_original_descriptor_path_and_type)
from server.resources.helpers.executions import (
    write_inputs_to_file, create_execution_directory, get_execution_as_model,
    validate_request_model, delete_execution_directory,
    copy_descriptor_to_execution_dir, create_absolute_path_inputs,
    query_converter)
from server.database.queries.executions import (get_all_executions_for_user,
                                                get_execution)
from .models.execution import ExecutionSchema
from .decorators import unmarshal_request, marshal_response, login_required
from server.resources.models.descriptor.descriptor_abstract import Descriptor


class Executions(Resource):
    @login_required
    @marshal_response(ExecutionSchema(many=True))
    def get(self, user):
        offset = request.args.get('offset', type=query_converter)
        limit = request.args.get(
            'limit', type=query_converter) or PLATFORM_PROPERTIES.get(
                'defaultLimitListExecutions')
        user_executions = get_all_executions_for_user(user.username, limit,
                                                      offset, db.session)
        for i, execution in enumerate(user_executions):
            exe, error = get_execution_as_model(user.username, execution)
            if error:
                return error
            user_executions[i] = exe

        return user_executions

    @login_required
    @unmarshal_request(ExecutionSchema())
    @marshal_response(ExecutionSchema())
    def post(self, model, user):
        _, error = validate_request_model(model, request.url_root)
        if error:
            return error

        try:
            # Get the descriptor path and type
            (descriptor_path,
             descriptor_type), error = get_original_descriptor_path_and_type(
                 model.pipeline_identifier)
            if error:
                return error

            # Insert new execution to DB
            new_execution = Execution(
                name=model.name,
                pipeline_identifier=model.pipeline_identifier,
                descriptor=descriptor_type,
                timeout=model.timeout,
                status=ExecutionStatus.Initializing,
                study_identifier=model.study_identifier,
                creator_username=user.username)
            db.session.add(new_execution)
            db.session.commit()

            # Execution directory creation
            (execution_path,
             carmin_files_path), error = create_execution_directory(
                 new_execution, user)
            if error:
                db.session.rollback()
                return error

            # Writing inputs to inputs file in execution directory
            error = write_inputs_to_file(model, carmin_files_path)
            if error:
                delete_execution_directory(execution_path)
                db.session.rollback()
                return error

            # Copying pipeline descriptor to execution folder
            error = copy_descriptor_to_execution_dir(carmin_files_path,
                                                     descriptor_path)
            if error:
                delete_execution_directory(execution_path)
                db.session.rollback()
                return UNEXPECTED_ERROR

            # Get appriopriate descriptor object
            descriptor = Descriptor.descriptor_factory_from_type(
                new_execution.descriptor)
            if not descriptor:
                delete_execution_directory(execution_path)
                db.session.rollback()
                # We don't have any descriptor defined for this pipeline type
                logger = logging.getLogger('server-error')
                logger.error(
                    "Unsupported descriptor type extracted from file at {}".
                    format(descriptor_path))
                return ErrorCodeAndMessageFormatter(
                    UNSUPPORTED_DESCRIPTOR_TYPE, descriptor_type)

            # Create a version of the inputs file with correct links
            modified_inputs_path, error = create_absolute_path_inputs(
                user.username, new_execution.identifier,
                new_execution.pipeline_identifier, request.url_root)
            if error:
                delete_execution_directory(execution_path)
                db.session.rollback()
                return UNEXPECTED_ERROR

            # We now validate the invocation
            success, error = descriptor.validate(descriptor_path,
                                                 modified_inputs_path)
            if not success:  # If this fails, we will change the execution status to InitializationFailed and return this error
                new_execution.status = ExecutionStatus.InitializationFailed
                db.session.commit()
                error_code_and_message = ErrorCodeAndMessageFormatter(
                    INVOCATION_INITIALIZATION_FAILED, new_execution.identifier)
                return ErrorCodeAndMessageAdditionalDetails(
                    error_code_and_message, str(error))

            # Get execution from DB (for safe measure)
            execution_db = get_execution(new_execution.identifier, db.session)
            if not execution_db:
                return UNEXPECTED_ERROR

            # Get execution back as a model from the DB for response
            execution, error = get_execution_as_model(user.username,
                                                      execution_db)
            if error:
                return UNEXPECTED_ERROR
            return execution
        except IntegrityError:
            db.session.rollback()
