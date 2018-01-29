from .base_model import Model
from server.common import util


class Path(Model):
    """Path

    Args:
        platform_path (str): A valid path, slash-separated. It must be consistent with the path of files and directories uploaded and downloaded by clients. For instance, if a user uploads a directory structure "dir/{file1.txt,file2.txt}", it is expected that the path of the first file will be "[prefix]/dir/file1.txt" and that the path of the second file will be "[prefix]/dir/file2.txt" where [prefix] depends on the upload parameters, in particular destination directory.
        last_modification_date (int): Date of last modification, in seconds since the Epoch (UNIX timestamp).
        is_directory (bool): True if the path represents a directory.
        size (int, optional): For a file, size in bytes. For a directory, sum of all the sizes of the files contained in the directory (recursively).
        execution_id (str, optional): Id of the Execution that produced the Path.
        mime_type (str, optional): mime type based on RFC 6838.

    Attributes:
        platform_path (str): A valid path, slash-separated. It must be consistent with the path of files and directories uploaded and downloaded by clients. For instance, if a user uploads a directory structure "dir/{file1.txt,file2.txt}", it is expected that the path of the first file will be "[prefix]/dir/file1.txt" and that the path of the second file will be "[prefix]/dir/file2.txt" where [prefix] depends on the upload parameters, in particular destination directory.
        last_modification_date (int): Date of last modification, in seconds since the Epoch (UNIX timestamp).
        is_directory (bool): True if the path represents a directory.
        size (int, optional): For a file, size in bytes. For a directory, sum of all the sizes of the files contained in the directory (recursively).
        execution_id (str, optional): Id of the Execution that produced the Path.
        mime_type (str, optional): mime type based on RFC 6838.
    """

    def __init__(self,
                 platform_path: str = None,
                 last_modification_date: int = None,
                 is_directory: bool = None,
                 size: int = None,
                 execution_id: str = None,
                 mime_type: str = None):

        self.swagger_types = {
            'platform_path': str,
            'last_modification_date': int,
            'is_directory': bool,
            'size': int,
            'execution_id': str,
            'mime_type': str
        }

        self.attribute_map = {
            'platform_path': 'platformPath',
            'last_modification_date': 'lastModificationDate',
            'is_directory': 'isDirectory',
            'size': 'size',
            'execution_id': 'executionId',
            'mime_type': 'mimeType'
        }

        self._platform_path = platform_path
        self._last_modification_date = last_modification_date
        self._is_directory = is_directory
        self._size = size
        self._execution_id = execution_id
        self._mime_type = mime_type

    @classmethod
    def from_dict(cls, dikt) -> 'Path':
        """Returns the dict as a model

        Args:
            dikt (dict): A dict.

        Returns:
            Path: The Path of this Path.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def platform_path(self) -> str:
        """Gets the platform_path of this Path.

        A valid path, slash-separated. It must be consistent with the path of files and directories uploaded and downloaded by clients. For instance, if a user uploads a directory structure \"dir/{file1.txt,file2.txt}\", it is expected that the path of the first file will be \"[prefix]/dir/file1.txt\" and that the path of the second file will be \"[prefix]/dir/file2.txt\" where [prefix] depends on the upload parameters, in particular destination directory.

        Returns:
            str: The platform_path of this Path.
        """
        return self._platform_path

    @platform_path.setter
    def platform_path(self, platform_path: str):
        """Sets the platform_path of this Path.

        A valid path, slash-separated. It must be consistent with the path of files and directories uploaded and downloaded by clients. For instance, if a user uploads a directory structure \"dir/{file1.txt,file2.txt}\", it is expected that the path of the first file will be \"[prefix]/dir/file1.txt\" and that the path of the second file will be \"[prefix]/dir/file2.txt\" where [prefix] depends on the upload parameters, in particular destination directory.

        Args:
            platform_path (str): The platform_path of this Path.
        """
        if platform_path is None:
            raise ValueError(
                "Invalid value for `platform_path`, must not be `None`")

        self._platform_path = platform_path

    @property
    def last_modification_date(self) -> int:
        """Gets the last_modification_date of this Path.

        Date of last modification, in seconds since the Epoch (UNIX timestamp).

        Returns:
            int: The last_modification_date of this Path.
        """
        return self._last_modification_date

    @last_modification_date.setter
    def last_modification_date(self, last_modification_date: int):
        """Sets the last_modification_date of this Path.

        Date of last modification, in seconds since the Epoch (UNIX timestamp).

        Args:
            last_modification_date (int): The last_modification_date of this Path.
        """
        if last_modification_date is None:
            raise ValueError(
                "Invalid value for `last_modification_date`, must not be `None`"
            )

        self._last_modification_date = last_modification_date

    @property
    def is_directory(self) -> bool:
        """Gets the is_directory of this Path.

        True if the path represents a directory.

        Returns:
            bool: The is_directory of this Path.
        """
        return self._is_directory

    @is_directory.setter
    def is_directory(self, is_directory: bool):
        """Sets the is_directory of this Path.

        True if the path represents a directory.

        Args:
            is_directory (bool): The is_directory of this Path.
        """
        if is_directory is None:
            raise ValueError(
                "Invalid value for `is_directory`, must not be `None`")

        self._is_directory = is_directory

    @property
    def size(self) -> int:
        """Gets the size of this Path.

        For a file, size in bytes. For a directory, sum of all the sizes of the files contained in the directory (recursively).

        Returns:
            int: The size of this Path.
        """
        return self._size

    @size.setter
    def size(self, size: int):
        """Sets the size of this Path.

        For a file, size in bytes. For a directory, sum of all the sizes of the files contained in the directory (recursively).

        Args:
            size (int): The size of this Path.
        """

        self._size = size

    @property
    def execution_id(self) -> str:
        """Gets the execution_id of this Path.

        Id of the Execution that produced the Path.

        Returns:
            str: The execution_id of this Path.
        """
        return self._execution_id

    @execution_id.setter
    def execution_id(self, execution_id: str):
        """Sets the execution_id of this Path.

        Id of the Execution that produced the Path.

        Args:
            execution_id (str): The execution_id of this Path.
        """

        self._execution_id = execution_id

    @property
    def mime_type(self) -> str:
        """Gets the mime_type of this Path.

        mime type based on RFC 6838.

        Returns:
            str: The mime_type of this Path.
        """
        return self._mime_type

    @mime_type.setter
    def mime_type(self, mime_type: str):
        """Sets the mime_type of this Path.

        mime type based on RFC 6838.

        Args:
            mime_type (str): The mime_type of this Path.
        """

        self._mime_type = mime_type
