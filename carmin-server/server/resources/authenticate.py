import random
import json
from server import db
from flask_restful import Resource, fields, marshal_with, request
from flask import make_response, jsonify, abort
from .models.authentication import Authentication, AuthenticationSchema
from .decorators import resource_model, custom_marshal_with


class Authenticate(Resource):
    @resource_model(AuthenticationSchema())
    @custom_marshal_with(AuthenticationSchema())
    def post(self, model):
        return model
