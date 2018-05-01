import os
from flask_restful import Resource, request
from jsonschema import ValidationError
from server.database import db
from server.database.queries.executions import get_execution
from server.resources.decorators import login_required, marshal_response
from server.database.models.execution import Execution, ExecutionStatus
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageFormatter, ErrorCodeAndMessageAdditionalDetails,
    EXECUTION_NOT_FOUND, UNAUTHORIZED, CORRUPTED_EXECUTION, UNEXPECTED_ERROR,
    CANNOT_REPLAY_EXECUTION, UNSUPPORTED_DESCRIPTOR_TYPE)
from server.resources.helpers.executions import (
    get_execution_as_model, get_descriptor_path, get_absolute_path_inputs_path)
from server.resources.helpers.execution_play import start_execution
from server.resources.models.descriptor.descriptor_abstract import Descriptor


class ExecutionPlay(Resource):
    @login_required
    @marshal_response()
    def put(self, user, execution_identifier):
        execution_db = get_execution(execution_identifier, db.session)
        if not execution_db:
            return ErrorCodeAndMessageFormatter(EXECUTION_NOT_FOUND,
                                                execution_identifier)
        if execution_db.creator_username != user.username:
            return UNAUTHORIZED

        if execution_db.status != ExecutionStatus.Initializing:
            return ErrorCodeAndMessageFormatter(CANNOT_REPLAY_EXECUTION,
                                                execution_db.status.name)

        execution, error = get_execution_as_model(user.username, execution_db)
        if error:
            return CORRUPTED_EXECUTION

        # Get the descriptor path
        descriptor_path = get_descriptor_path(user.username,
                                              execution.identifier)

        # Get appriopriate descriptor object
        descriptor = Descriptor.descriptor_factory_from_type(
            execution_db.descriptor)

        if not descriptor:
            # We don't have any descriptor defined for this pipeline type
            logger = logging.getLogger('server-error')
            logger.error(
                "Unsupported descriptor type extracted from file at {}".format(
                    descriptor_path))
            return ErrorCodeAndMessageFormatter(UNSUPPORTED_DESCRIPTOR_TYPE,
                                                execution_db.descriptor)

        modified_inputs_path = get_absolute_path_inputs_path(
            user.username, execution.identifier)
        if not os.path.isfile(modified_inputs_path):
            logger = logging.getLogger('server-error')
            logger.error("Absolute path inputs file not found at {}".format(
                descriptor_path))
            return UNEXPECTED_ERROR

        # The execution is valid and we are now ready to start it
        start_execution(user, execution, descriptor, modified_inputs_path)
