from flask_restful import Resource
from server.resources.helpers.std import std_file_resource
from server.resources.helpers.executions import STDERR_FILENAME
from server.resources.decorators import login_required


class ExecutionStdErr(Resource):
    @login_required
    def get(self, user, execution_identifier):
        return std_file_resource(user, execution_identifier, STDERR_FILENAME)
