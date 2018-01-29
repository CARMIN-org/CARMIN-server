from flask_restful import Resource
from .models.platform_properties import PlatformProperties


class Platform(Resource):
    def get(self):
        return PlatformProperties().to_dict()
