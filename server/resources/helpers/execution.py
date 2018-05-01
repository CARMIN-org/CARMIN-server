import os
from pathlib import PurePath
from server import app
from server.resources.helpers.pathnames import EXECUTIONS_DIRNAME


def extract_execution_identifier_from_path(
        absolute_path_to_resource: str) -> str:

    rel_path = PurePath(
        os.path.relpath(absolute_path_to_resource,
                        app.config['DATA_DIRECTORY'])).as_posix()

    normalized_path = os.path.normpath(rel_path)
    split_path = normalized_path.split(os.sep)

    try:
        executions_folder_index = split_path.index(EXECUTIONS_DIRNAME)
        # The execution folder should be at the root of the user data directory
        # Otherwise, this is not an execution
        if executions_folder_index != 1:
            return None

        actual_execution_folder_index = executions_folder_index + 1

        if len(split_path) < actual_execution_folder_index + 1:
            return None
        elif len(split_path) == actual_execution_folder_index + 1:
            # We have an execution folder
            if os.path.isdir(absolute_path_to_resource):
                return split_path[actual_execution_folder_index]
            else:
                return None
        else:
            return split_path[actual_execution_folder_index]
    except ValueError:
        return None
