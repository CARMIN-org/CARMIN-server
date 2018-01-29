from server.common import util
from .base_model import Model


class BooleanResponse(Model):
    """A boolean response for "exists" action "getPath" operation

    Args:
        exists (bool):
    Attributes:
        exists (bool):
    """

    def __init__(self, exists: bool = None):
        self.swagger_type = {'exists': bool}
        self.attribute_map = {'exists': 'exists'}
        self._exists = exists

    @classmethod
    def from_dict(cls, dikt) -> 'BooleanResponse':
        """Return the dict as a model.

        Args:
            dikt (dict): A dictionary.
        Returns:
            BooleanResponse: The BooleanResponse generated from the dict.
        """
        return util.deserialize_model(dikt, cls)
