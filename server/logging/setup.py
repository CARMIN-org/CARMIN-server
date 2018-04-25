import re
import traceback
import logging
import logging.config
from flask import g, request, got_request_exception, jsonify
from server import app
from server.logging.config import LOGGING_CONFIG
from server.common.error_codes_and_messages import ErrorCodeAndMessageMarshaller, PAGE_NOT_FOUND
from server.test.utils import error_from_response

logging.config.dictConfig(LOGGING_CONFIG)

# Using this instead of @app.errorhandler since flask-restful does not support
# the decorator.


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(ErrorCodeAndMessageMarshaller(PAGE_NOT_FOUND)), 404


def log_exception(sender, exception, **extra):
    logger = logging.getLogger('server-error')
    logger.error(traceback.format_exc())


got_request_exception.connect(log_exception, app)


@app.after_request
def log_response(response):
    logger = logging.getLogger('request-response')
    user_error = re.compile("^4").match(response.status)
    server_error = re.compile("^5").match(response.status)

    if user_error or server_error:
        request_content = request.get_json()
        if request_content and request_content.get('password'):
            request_content['password'] = '[password]'

        if user_error:
            msg = '\n  User: - IP: {}, username: {}\n  Method - {} {}\n  Request - {}\n  Response - {}'.format(
                request.remote_addr, g.get('username'), request.method,
                request.path, request_content, response.get_data())
            logger.warning(msg)
        elif server_error:
            msg = '\n  User: - {}\n  Method - {} {}\n  Request - {}\n  Response - {}'.format(
                request.remote_addr, request.method, request.path,
                request_content, response.get_data())
            logger.error(msg)
    else:
        msg = '{} - {} - {}'.format(request.remote_addr, request.path,
                                    response.status)
        logger.info(msg)
    return response
