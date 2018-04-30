"""Properties Validation performs validation on the `server-config.json` file,
which contains a description of the PlatformProperties object.
"""
import os
import sys
import json
import string
import random
from typing import Dict
from .config import (SQLITE_DEFAULT_PROD_DB_URI, DEFAULT_PROD_DB_URI)
from .resources.models.platform_properties import PlatformPropertiesSchema
from server import app
from server.database import db
from .database.models.user import User, Role
from .database.models.execution import Execution, ExecutionStatus
from .database.models.execution_process import ExecutionProcess
from .database.queries.executions import get_execution_processes
from server.resources.helpers.pipelines import export_all_pipelines
from server.common.error_codes_and_messages import PATH_EXISTS
from server.resources.models.descriptor.supported_descriptors import SUPPORTED_DESCRIPTORS
from server.platform_properties import PLATFORM_PROPERTIES
from server.resources.helpers.execution_kill import (get_process_alive_count,
                                                     kill_execution_processes)


def start_up():
    create_dirs_for_supported_descriptors()
    pipeline_and_data_directory_present()
    export_pipelines()
    properties_validation()
    find_or_create_admin()
    purge_executions()


def properties_validation(config_data: Dict = None) -> bool:
    """Performs validation on server_config.json file. Checks for required
    parameters and supported options."""

    if not config_data:
        config_data = PLATFORM_PROPERTIES
    platform_properties, err = PlatformPropertiesSchema().load(config_data)

    # Raise error if required property is not provided
    if err:
        raise EnvironmentError(err)

    # Raise error if https not in supported protocols
    if "https" not in platform_properties.supported_transfer_protocols:
        raise EnvironmentError('CARMIN 0.3 requires https support')

    # Raise error if minTimeout is greater than maxTimeout
    if (platform_properties.max_authorized_execution_timeout != 0
            and platform_properties.min_authorized_execution_timeout >
            platform_properties.max_authorized_execution_timeout):
        raise ValueError('maxTimeout must be greater than minTimeout')
    return True


def pipeline_and_data_directory_present():
    """Checks if Pipeline and Data directories were specified at launch. If not,
    raise EnvironmentError
    """
    PIPELINE_DIRECTORY = app.config['PIPELINE_DIRECTORY']
    DATA_DIRECTORY = app.config['DATA_DIRECTORY']

    if not PIPELINE_DIRECTORY:
        raise EnvironmentError(
            "ENV['PIPELINE_DIRECTORY'] must be set to Pipeline directory path")
    if not DATA_DIRECTORY:
        raise EnvironmentError(
            "ENV['DATA_DIRECTORY'] must be set to input Data directory path")

    if app.config['SQLALCHEMY_DATABASE_URI'] == SQLITE_DEFAULT_PROD_DB_URI:
        print(
            "No SQL database URI found. Reverting to default production database found at {}".
            format(DEFAULT_PROD_DB_URI),
            flush=True)

    if (not os.path.isdir(PIPELINE_DIRECTORY)
            or not os.path.isdir(DATA_DIRECTORY)):
        raise EnvironmentError(
            "Data and Pipeline directories must be valid. Make sure that the given paths are absolute."
        )


def find_or_create_admin():
    admin = db.session.query(User).filter_by(role=Role.admin).first()
    if not admin:
        admin_username = "admin"
        admin_password = generate_admin_password()
        result, error = register_user(admin_username, admin_password,
                                      Role.admin, db.session)

        if error:
            raise EnvironmentError("Could not create first admin account.")
        separator = '-' * 20
        print('{0} Admin Account {0}\nusername: {1}\npassword: {2}\n'.format(
            separator, admin_username, admin_password))


def generate_admin_password(password_length=16):
    return ''.join(
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(password_length))


def export_pipelines():
    success, error = export_all_pipelines()

    if not success:
        raise EnvironmentError(error)


def create_dirs_for_supported_descriptors():
    pipeline_path = app.config['PIPELINE_DIRECTORY']
    for key in SUPPORTED_DESCRIPTORS:
        try:
            os.mkdir(os.path.join(pipeline_path, key))
        except FileExistsError:
            pass
        except OSError:
            raise EnvironmentError(
                "Directory '{}' could not be created. This problem could be due to insufficient disk space.".
                format(key))


def purge_executions():
    # Let's get all executions running
    executions = db.session.query(Execution).filter_by(
        status=ExecutionStatus.Running)

    for e in executions:
        # Look at if it has some processes linked to it
        execution_processes = get_execution_processes(e.identifier, db.session)

        if not execution_processes:  # Most probably due to the execution being in termination process
            continue

        actual_execution_processes = [
            e for e in execution_processes if e.is_execution
        ]
        execution_parent_processes = [
            e for e in execution_processes if not e.is_execution
        ]

        process_still_alive_count = 0
        process_still_alive_count += get_process_alive_count(
            actual_execution_processes)
        process_still_alive_count += get_process_alive_count(
            execution_parent_processes)

        # The execution is going as expected
        if process_still_alive_count == len(execution_processes):
            continue

        # The execution is supposed to be still running but some of the processes it launched are no more active
        # We will mark the execution as "ExecutionFailed" and kill the remaining processes
        kill_execution_processes(execution_parent_processes)
        kill_execution_processes(actual_execution_processes)

        e.status = ExecutionStatus.Unknown
        for execution_process in execution_processes:
            db.session.delete(execution_process)
        db.session.commit()

    # Now that the executions marked as 'Running' have been purged, let's clean up the remaining execution processes
    remaining_processes = db.session.query(ExecutionProcess)
    for process in remaining_processes:
        kill_execution_processes([process])
        db.session.delete(process)
        db.session.commit()


from server.resources.helpers.register import register_user
