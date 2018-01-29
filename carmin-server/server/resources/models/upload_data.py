from .base_model import Model
from server.common import util


class UploadData(Model):
    """UploadData

    Args:
        base64_content (str): The base64_content of this UploadData.
        upload_type (str): The type of this UploadData.
        md5 (str, optional): The md5 of this UploadData.

    Attributes:
        base64_content (str): The base64_content of this UploadData.
        upload_type (str): The type of this UploadData.
        md5 (str, optional): The md5 of this UploadData.
    """

    def __init__(self,
                 base64_content: str = None,
                 upload_type: str = None,
                 md5: str = None):

        self.swagger_types = {
            'base64_content': str,
            'upload_type': str,
            'md5': str
        }

        self.attribute_map = {
            'base64_content': 'base64Content',
            'upload_type': 'type',
            'md5': 'md5'
        }

        self._base64_content = base64_content
        self._upload_type = upload_type
        self._md5 = md5

    @classmethod
    def from_dict(cls, dikt) -> 'UploadData':
        """Returns the dict as a model

        Args:
            dikt (dict): A dict.

        Returns:
            UploadData: The UploadData of this UploadData.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def base64_content(self) -> str:
        """Gets the base64_content of this UploadData.

        If the type is \"File\", the base64 string will be decoded to a single raw file. If the type is \"Archive\", the base64 string must corresponds to an encoded zip file that will be decoded to create directory and its content.

        Returns:
            str: The base64_content of this UploadData.
        """
        return self._base64_content

    @base64_content.setter
    def base64_content(self, base64_content: str):
        """Sets the base64_content of this UploadData.

        If the type is \"File\", the base64 string will be decoded to a single raw file. If the type is \"Archive\", the base64 string must corresponds to an encoded zip file that will be decoded to create directory and its content.

        Args:
            base64_content (str): The base64_content of this UploadData.
        """
        if base64_content is None:
            raise ValueError(
                "Invalid value for `base64_content`, must not be `None`")

        self._base64_content = base64_content

    @property
    def upload_type(self) -> str:
        """Gets the type of this UploadData.

        Returns:
            str: The type of this UploadData.
        """
        return self._upload_type

    @upload_type.setter
    def upload_type(self, upload_type: str):
        """Sets the type of this UploadData.

        Args:
            upload_type (str): The type of this UploadData.
        """
        allowed_values = ["File", "Archive"]
        if upload_type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}".format(
                    upload_type, allowed_values))

        self._upload_type = upload_type

    @property
    def md5(self) -> str:
        """Gets the md5 of this UploadData.

        Returns:
            str: The md5 of this UploadData.
        """
        return self._md5

    @md5.setter
    def md5(self, md5: str):
        """Sets the md5 of this UploadData.

        Args:
            md5 (str): The md5 of this UploadData.
        """

        self._md5 = md5
