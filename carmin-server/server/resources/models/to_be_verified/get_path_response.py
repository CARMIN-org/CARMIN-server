# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime

from typing import List, Dict

from server.models.base_model import Model

from server.models.boolean_response import BooleanResponse
from server.models.path import Path
from server.models.directory_list import DirectoryList
from server.models.path_md5 import PathMD5

from server import util


class GetPathResponse(Model):
    """GetPathResponse
    """

    def __init__(self):
        """GetPathResponse - a model defined in Swagger

        """
        self.swagger_types = {}

        self.attribute_map = {}

    @classmethod
    def from_dict(cls, dikt) -> 'GetPathResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The GetPathResponse of this GetPathResponse.  # noqa: E501
        :rtype: GetPathResponse
        """
        return util.deserialize_model(dikt, cls)
