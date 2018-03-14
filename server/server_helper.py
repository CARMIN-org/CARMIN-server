import os
from flask import Flask
from flask_restful import Api

from server.database import db
from server.config import Config


def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.from_object(config)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    return app


def declare_api(app):

    api = Api(app)
    from server.startup_validation import start_up
    from server.resources.authenticate import Authenticate
    from server.resources.register import Register
    from server.resources.executions import Executions
    from server.resources.execution import Execution
    from server.resources.execution_kill import ExecutionKill
    from server.resources.execution_play import ExecutionPlay
    from server.resources.execution_stderr import ExecutionStdErr
    from server.resources.execution_stdout import ExecutionStdOut
    from server.resources.execution_results import ExecutionResults
    from server.resources.executions_count import ExecutionsCount
    from server.resources.path import Path
    from server.resources.pipeline import Pipeline
    from server.resources.pipelines import Pipelines
    from server.resources.platform import Platform

    api.add_resource(Platform, '/platform')
    api.add_resource(Authenticate, '/authenticate')
    api.add_resource(Register, '/users/register')
    api.add_resource(Executions, '/executions')
    api.add_resource(ExecutionsCount, '/executions/count')
    api.add_resource(Execution, '/executions/<string:execution_identifier>')
    api.add_resource(ExecutionResults,
                     '/executions/<string:execution_identifier>/results')
    api.add_resource(ExecutionStdOut,
                     '/executions/<string:execution_identifier>/stdout')
    api.add_resource(ExecutionStdErr,
                     '/executions/<string:execution_identifier>/stderr')
    api.add_resource(ExecutionPlay,
                     '/executions/<string:execution_identifier>/play')
    api.add_resource(ExecutionKill,
                     '/executions/<string:execution_identifier>/kill')
    api.add_resource(Pipelines, '/pipelines')
    api.add_resource(Pipeline, '/pipelines/<string:pipeline_identifier>')
    api.add_resource(Path, '/path/<path:complete_path>', '/path/')