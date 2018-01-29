from .base_model import Model
from server.common import util


class ParameterType(Model):
    """Enum representing a Parameter type
    """
    FILE = "File"
    STRING = "String"
    BOOLEAN = "Boolean"
    INT64 = "Int64"
    DOUBLE = "Double"
    LIST = "List"

    @classmethod
    def from_dict(cls, dikt) -> 'ParameterType':
        return util.deserialize_model(dikt, cls)
