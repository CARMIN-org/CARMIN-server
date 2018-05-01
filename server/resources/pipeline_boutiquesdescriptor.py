import os
import json
from flask_restful import Resource
from server.common.utils import marshal
from .models.error_code_and_message import ErrorCodeAndMessage
from .decorators import login_required
from server.resources.helpers.pipelines import get_original_descriptor_path_and_type, get_descriptor_json


class PipelineBoutiquesDescriptor(Resource):

    # No need for marshal response as the payload is a simple JSON dump of the Boutiques descriptor
    # Moreover, there is no BoutiquesSchema yet. If it was to be added, this should be changed.
    @login_required
    def get(self, user, pipeline_identifier):
        (boutiques_descriptor_path, descriptor_type
         ), error = get_original_descriptor_path_and_type(pipeline_identifier)

        if error:
            return marshal(error), 400

        boutiques_descriptor, error = get_descriptor_json(
            boutiques_descriptor_path)

        if error:
            return marshal(error), 400

        return boutiques_descriptor, 200
