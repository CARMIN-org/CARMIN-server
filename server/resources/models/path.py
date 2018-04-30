import os
from pathlib import PurePath
import mimetypes
from server import app
from flask_restful import request
from marshmallow import Schema, fields, post_load, post_dump
from server.resources.helpers.execution import extract_execution_identifier_from_path


class PathSchema(Schema):
    SKIP_VALUES = set([None])

    class Meta:
        ordered = True

    platform_path = fields.Str(
        required=True, dump_to='platformPath', load_from='platformPath')
    last_modification_date = fields.Int(
        required=True,
        dump_to='lastModificationDate',
        load_from='lastModificationDate')
    is_directory = fields.Bool(
        required=True, dump_to='isDirectory', load_from='isDirectory')
    size = fields.Int()
    execution_id = fields.Str(dump_to='executionId', load_from='executionId')
    mime_type = fields.Str(dump_to='mimeType', load_from='mimeType')

    @post_load
    def to_model(self, data):
        return Path(**data)

    @post_dump
    def remove_skip_values(self, data):
        """remove_skip_values removes all values specified in the
        SKIP_VALUES set from appearing in the 'dumped' JSON.
        """
        return {
            key: value
            for key, value in data.items() if value not in self.SKIP_VALUES
        }


class Path():
    """Path represents a filesystem resource (file or directory).

    Attributes:
        platform_path (str): The url where the Path can be found.
        last_modification_date (int): Date of last modification, in seconds
        since the Epoch (UNIX timestamp).
        is_directory (bool): True if the path represents a directory.
        size (int): For a file, size in bytes. For a directory, sum of all the
        sizes of the files contained in the directory (recursively).
        execution_id (str): ID of the execution that produced the Path.
        mime_type (str): MIME type based on RFC 6838.
    """
    schema = PathSchema()

    def __init__(self,
                 platform_path: str,
                 last_modification_date: int,
                 is_directory: bool,
                 size: int = None,
                 execution_id: str = None,
                 mime_type: str = None):
        self.platform_path = platform_path
        self.last_modification_date = last_modification_date
        self.is_directory = is_directory
        self.size = size
        self.execution_id = execution_id
        self.mime_type = mime_type

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @classmethod
    def object_from_pathname(cls, absolute_path_to_resource: str):
        """object_from_pathname takes the path of the platform data root directory
        as its first argument, and the path of the requested resource
        relative to the root directory as second argument. It then returns a
        Path object based on the associated file or directory.
        """

        is_directory = os.path.isdir(absolute_path_to_resource)
        mime_type = None

        if not is_directory:
            mime_type, _ = mimetypes.guess_type(absolute_path_to_resource)

        # TODO: Add execution_id to Path object
        execution_id = extract_execution_identifier_from_path(
            absolute_path_to_resource)

        rel_path = PurePath(
            os.path.relpath(absolute_path_to_resource,
                            app.config['DATA_DIRECTORY'])).as_posix()

        return Path(
            platform_path='{}path/{}'.format(request.url_root, rel_path),
            last_modification_date=os.path.getmtime(absolute_path_to_resource),
            is_directory=os.path.isdir(absolute_path_to_resource),
            size=Path.get_path_size(absolute_path_to_resource, is_directory),
            mime_type=mime_type,
            execution_id=execution_id)

    @classmethod
    def get_path_size(cls, absolute_path: str, is_dir: bool) -> int:
        """get_path_size returns the size of the resource.

        Attributes:
            absolute_path (str): Absolute path to the resource.
            is_dir (bool): True if the resource is a directory.
        Returns:
            (int): Size of the resource.
        """
        size = 0
        if is_dir:
            for dirpath, _, filenames in os.walk(absolute_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    size += os.path.getsize(fp)
        else:
            size = os.path.getsize(absolute_path)
        return size
