import os
from flask_restful import Resource, request
from server.common.error_codes_and_messages import MISSING_PIPELINE_PROPERTY
from .models.pipeline import PipelineSchema
from .decorators import login_required, marshal_response
from .helpers.pipelines import pipelines


class Pipelines(Resource):
    @login_required
    @marshal_response(PipelineSchema(many=True))
    def get(self, user):
        study_identifier = request.args.get('studyIdentifier')
        pipeline_property = request.args.get('property')
        property_value = request.args.get('propertyValue')

        if property_value and not pipeline_property:
            return MISSING_PIPELINE_PROPERTY

        return pipelines(None, study_identifier, pipeline_property,
                         property_value)
