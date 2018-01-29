from typing import List
from .base_model import Model
from .path import Path
from server.common import util


class DirectoryList(Model):
    """DirectoryList
    
    Attributes:
        directories List[Path]:

    Args:
        directories List[Path]:
    """

    def __init__(self, directories: List[Path] = None):
        self.swagger_types = {'directories': List[Path]}

        self.attribute_map = {'directories': 'directories'}

        self._directories = directories

    @classmethod
    def from_dict(cls, dikt) -> 'DirectoryList':
        """Returns the dict as a model

        Args:
            dikt (dict):
        
        Returns:
           DirectoryList: The DirectoryList of this DirectoryList.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def directories(self) -> str:
        """Gets the directories of this DirectoryList

        Returns:
            List[Path]: The directories of this DirectoryList.
        """
        return self._directories

    @directories.setter
    def directories(self, directories: List[Path]):
        """Sets the directories of this DirectoryList.

        Args:
            
        """
        if directories is None:
            raise ValueError(
                "Invalid value for `directories`, must not be `None`")

        self._directories = directories
