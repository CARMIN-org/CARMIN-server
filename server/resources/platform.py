from flask_restful import Resource
from server.platform_properties import PLATFORM_PROPERTIES
from server.resources.models.platform_properties import PlatformPropertiesSchema
from server.resources.decorators import marshal_response


class Platform(Resource):
    @marshal_response(PlatformPropertiesSchema())
    def get(self):
        return PlatformPropertiesSchema().load(PLATFORM_PROPERTIES).data
