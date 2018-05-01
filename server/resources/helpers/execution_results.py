import os
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk
from typing import List
from server.resources.helpers.executions import CARMIN_FILES_FOLDER, get_execution_dir
from server.resources.models.error_code_and_message import ErrorCodeAndMessage
from server.resources.models.path import Path


def get_output_files(username: str, execution_identifier: str
                     ) -> (List[str], ErrorCodeAndMessage):
    try:
        execution_dir = get_execution_dir(username, execution_identifier)
    except FileNotFoundError:
        return None, PATH_DOES_NOT_EXIST

    excluded_dirs = [CARMIN_FILES_FOLDER]
    output_files = list()
    for root, dirs, files in walk(execution_dir):
        dirs[:] = [d for d in dirs if d not in CARMIN_FILES_FOLDER]

        for f in files:
            real_path = os.path.realpath(os.path.join(root, f))
            output_files.append(Path.object_from_pathname(real_path))

    return output_files, None
