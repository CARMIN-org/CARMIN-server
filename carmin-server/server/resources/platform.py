import os
import json
from flask_restful import Resource
from .decorators import resource_model, custom_marshal_with
from .models.platform_properties import PlatformProperties, PlatformPropertiesSchema
from .models.error_code_and_message import ErrorCodeAndMessageSchema


class Platform(Resource):
    @custom_marshal_with(PlatformPropertiesSchema())
    def get(self):
        config_file = os.path.join(
            os.path.dirname(__file__), '../server-config.json')
        with open(config_file) as config_data:
            platform_properties, errors = PlatformPropertiesSchema().load(
                json.load(config_data))
            if errors:
                print(errors)
            return platform_properties
