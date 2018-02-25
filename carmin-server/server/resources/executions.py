import os
import json
from flask_restful import Resource
from .models.execution import Execution, ExecutionSchema
from server import app
from server.database.models.execution import Execution, ExecutionStatus
from .decorators import unmarshal_request, marshal_response, login_required
from server.common.error_codes_and_messages import EXECUTION_IDENTIFIER_MUST_NOT_BE_SET
from server.resources.helpers.executions import write_inputs_to_file


class Executions(Resource):
    def get(self):
        pass

    @login_required
    @unmarshal_request(ExecutionSchema())
    @marshal_response(ExecutionSchema())
    def post(self, model, user):
        if (model.identifier):
            return EXECUTION_IDENTIFIER_MUST_NOT_BE_SET

        # TODO: Validate that the pipeline_identifier is valid

        # TODO: If study_identifier is set, validate it exists

        new_execution = Execution(
            name=model.name,
            pipeline_identifier=model.pipeline_identifier,
            timeout=model.timeout,
            status=ExecutionStatus.Initializing,
            study_identifier=model.study_identifier)

        #  write_inputs_to_file(model, user_execution_dir)
        return model
