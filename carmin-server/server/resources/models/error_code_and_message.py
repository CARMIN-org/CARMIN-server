from server.common import util
from .base_model import Model


class ErrorCodeAndMessage(Model):
    """ErrorCodeAndMessage contains a human readable error message
    along with a numerical error code.

    Attributes:
        error_code (int): Error code
        error_message (str): Human readable string describing the error.
    """

    def __init__(self, error_code: int = None, error_message: str = None):
        self.swagger_type = {'error_code': int, 'error_message': str}
        self.attribute_map = {
            'error_code': 'error_code',
            'error_message': 'error_message'
        }
        self._error_code = error_code
        self._error_message = error_message

    @classmethod
    def from_dict(cls, dikt) -> 'ErrorCodeAndMessage':
        """Return the dict as a model.

        Args:
            dikt (dict): A dictionary.
        Returns:
            ErrorCodeAndMessage: The ErrorCodeAndMessage generated from the dict.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def error_code(self) -> int:
        """Gets the code of this ErrorCodeAndMessage.

        Returns:
            int: The error code of this ErrorCodeAndMessage.
        """
        return self._error_code

    @error_code.setter
    def error_code(self, error_code: int):
        """Sets the code of this ErrorCodeAndMessage.

        Args:
            error_code (int): The error code of this ErrorCodeAndMessage.
        Raises:
            ValueError: If `error_code` is `None`.
        """
        if error_code is None:
            raise ValueError(
                "Invalid value for `error_code`, must not be `None`")
        self._error_code = error_code

    @property
    def error_message(self) -> str:
        """Gets the message of this ErrorCodeAndMessage.

        Returns:
            str: The human readable message of this ErrorCodeAndMessage.
        """
        return self._error_message

    @error_message.setter
    def error_message(self, error_message: str):
        """Sets the message of this ErrorCodeAndMessage.

        Args:
            error_message (str): The human readable message of this
            ErrorCodeAndMessage.
        Raises:
            ValueError: If `error_message` is `None`.
        """
        if error_message is None:
            raise ValueError(
                "Invalid value for `error_message`, must not be `None`")
        self._error_message = error_message
