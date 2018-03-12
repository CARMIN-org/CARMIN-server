import os
import json
from flask_restful import Resource
from .models.pipeline import Pipeline, PipelineSchema
from .decorators import marshal_response
from .helpers.pipelines import pipelines


class Pipeline(Resource):
    @marshal_response(PipelineSchema())
    def get(self, pipeline_identifier):
        pipeline = pipelines(pipeline_identifier)
        return next(iter(pipeline), {})
