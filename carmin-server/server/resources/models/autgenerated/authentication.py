from server.common.models.base_model import Model
from server.common import util


class Authentication(Model):
    """Authentication contains an HTTP Header name along with its value.

    Attributes:
        http_header (str): The HTTP Header name.
        http_header_value (str): The associated HTTP Header value.
    """

    def __init__(self, http_header: str = None, http_header_value: str = None):
        self.swagger_types = {'http_header': str, 'http_header_value': str}
        self.attribute_map = {
            'http_header': 'httpHeader',
            'http_header_value': 'httpHeaderValue'
        }
        self._http_header = http_header
        self._http_header_value = http_header_value

    @classmethod
    def from_dict(cls, dikt) -> 'Authentication':
        """Returns the dict as a model

        Args:
            dikt (dict): A dict.
        Returns:
           Authentication: The Authentication of this Authentication.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def http_header(self) -> str:
        """Gets the HTTP Header name of this Authentication.

        Returns:
            str: The http_header of this Authentication.
        """
        return self._http_header

    @http_header.setter
    def http_header(self, http_header: str):
        """Sets the HTTP Header name of this Authentication.

        Args:
            http_header (str): The http_header of this Authentication.
        """
        self._http_header = http_header

    @property
    def http_header_value(self) -> str:
        """Gets the http_header_value of this Authentication.

        Returns:
            str: The http_header_value of this Authentication.
        """
        return self._http_header_value

    @http_header_value.setter
    def http_header_value(self, http_header_value: str):
        """Sets the http_header_value of this Authentication.

        Args:
            http_header_value (str): The http_header_value of this Authentication.
        """
        self._http_header_value = http_header_value
