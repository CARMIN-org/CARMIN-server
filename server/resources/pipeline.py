import os
import json
from flask_restful import Resource
from server.common.error_codes_and_messages import INVALID_PIPELINE_IDENTIFIER
from .models.error_code_and_message import ErrorCodeAndMessage
from .models.pipeline import Pipeline, PipelineSchema
from .decorators import login_required, marshal_response
from .helpers.pipelines import pipelines


class Pipeline(Resource):
    @login_required
    @marshal_response(PipelineSchema())
    def get(self, user, pipeline_identifier):
        pipeline = pipelines(pipeline_identifier)
        if isinstance(pipeline, ErrorCodeAndMessage):
            return pipeline
        return next(iter(pipeline), INVALID_PIPELINE_IDENTIFIER)
