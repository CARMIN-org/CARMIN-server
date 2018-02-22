from server.resources.models.error_code_and_message import ErrorCodeAndMessage, ErrorCodeAndMessageSchema


def ErrorCodeAndMessageMarshaller(error_code_and_message: ErrorCodeAndMessage):
    return ErrorCodeAndMessageSchema().dump(error_code_and_message).data


GENERIC_ERROR = ErrorCodeAndMessage(0,
                                    "Something went wrong. Please try again.")
UNAUTHORIZED = ErrorCodeAndMessage(1, "Unauthorized access")
INVALID_PATH = ErrorCodeAndMessage(2, "Invalid pathname")
INVALID_ACTION = ErrorCodeAndMessage(3, "Invalid action")
MD5_ON_DIR = ErrorCodeAndMessage(
    4, "Invalid input: cannot generate md5 from directory")
LIST_ACTION_ON_FILE = ErrorCodeAndMessage(
    5, "Invalid input: cannot use list action on a file")
INVALID_MODEL_PROVIDED = ErrorCodeAndMessage(10, "Invalid model provided")
MODEL_DUMPING_ERROR = ErrorCodeAndMessage(15)
MISSING_API_KEY = ErrorCodeAndMessage(20, "Missing HTTP header field apiKey")
INVALID_API_KEY = ErrorCodeAndMessage(25, "Invalid apiKey")
INVALID_USERNAME_OR_PASSWORD = ErrorCodeAndMessage(
    30, "Invalid username/password.")
MISSING_PIPELINE_PROPERTY = ErrorCodeAndMessage(
    35, "'property' must be specified to use the 'propertyValue' argument")
USERNAME_ALREADY_EXISTS = ErrorCodeAndMessage(40,
                                              "Username '{}' already exists")
