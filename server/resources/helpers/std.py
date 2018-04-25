from flask import Response
from server.database import db
from server.common.utils import marshal
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageFormatter, EXECUTION_NOT_FOUND)
from server.database.queries.executions import get_execution
from server.resources.helpers.executions import (get_execution_as_model,
                                                 get_std_file, STDERR_FILENAME)
from server.resources.decorators import login_required


def std_file_resource(user, execution_identifier, path_to_file):
    execution_db = get_execution(execution_identifier, db.session)
    if not execution_db:
        error = ErrorCodeAndMessageFormatter(EXECUTION_NOT_FOUND,
                                             execution_identifier)
        return marshal(error), 400
    execution, error = get_execution_as_model(user.username, execution_db)
    if error:
        return marshal(error), 400

    std, error = get_std_file(user.username, execution_identifier,
                              path_to_file)
    if error:
        return marshal(error), 400

    return Response(std, mimetype='text/plain')
