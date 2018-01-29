from server.common import util
from .base_model import Model


class PathMD5(Model):
    """PathMD5

    Args:
        md5 (str):

    Attributes:
        md5 (str):

    """

    def __init__(self, md5: str = None):
        self.swagger_types = {'md5': str}
        self.attribute_map = {'md5': 'md5'}
        self._md5 = md5

    @classmethod
    def from_dict(cls, dikt) -> 'PathMD5':
        """Returns the dict as a model

        Args:  
            dikt (dict): A dict.
        
        Returns:
            PathMD5: The PathMD5 of this PathMD5.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def md5(self) -> str:
        """Gets the md5 of this PathMD5.

        Returns:
            str: The md5 of this PathMD5.
        """
        return self._md5

    @md5.setter
    def md5(self, md5: str):
        """Sets the md5 of this PathMD5.

        Args:
            md5 (str): The md5 of this PathMD5.
        """
        if md5 is None:
            raise ValueError("Invalid value for `md5`, must not be `None`")

        self._md5 = md5
