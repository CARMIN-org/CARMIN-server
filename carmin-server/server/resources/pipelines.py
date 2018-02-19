import os
import json
from flask_restful import Resource, request
from .models.pipeline import Pipeline, PipelineSchema
from .decorators import marshal_response
from server.common.pipeline_filter import pipelines
from server.common.error_codes_and_messages import MISSING_PIPELINE_PROPERTY


class Pipelines(Resource):
    @marshal_response(PipelineSchema(many=True))
    def get(self):
        study_identifier = request.args.get('studyIdentifier')
        pipeline_property = request.args.get('property')
        property_value = request.args.get('propertyValue')

        if (property_value and not pipeline_property):
            return MISSING_PIPELINE_PROPERTY

        return pipelines(None, study_identifier, pipeline_property,
                         property_value)
