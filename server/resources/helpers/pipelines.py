import os
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk
import json
import logging
from boutiques import bosh
from server import app
from server.resources.models.descriptor.descriptor_abstract import Descriptor
from server.resources.models.descriptor.supported_descriptors import SUPPORTED_DESCRIPTORS
from server.resources.models.pipeline import Pipeline, PipelineSchema
from server.common.error_codes_and_messages import (
    ErrorCodeAndMessageAdditionalDetails, ErrorCodeAndMessageFormatter,
    INVALID_PIPELINE_IDENTIFIER, UNEXPECTED_ERROR, PATH_DOES_NOT_EXIST)
from server.resources.models.error_code_and_message import ErrorCodeAndMessage


def pipelines(pipeline_identifier: str = None,
              study_identifier: str = None,
              pipeline_property: str = None,
              property_value: str = None):
    response = []
    pipeline_path = app.config['PIPELINE_DIRECTORY']
    for subdir, dirs, files in walk(pipeline_path):
        if study_identifier:
            dirs[:] = [i for i in dirs if i == study_identifier]

        # We exclude the descriptor folders as they include the
        # original, non-converted descriptors
        dirs[:] = [i for i in dirs if i not in SUPPORTED_DESCRIPTORS.keys()]

        for file in files:
            real_path = os.path.realpath(os.path.join(subdir, file))
            if file.endswith(".json"):
                with open(real_path) as pipeline_json:
                    pipeline, errors = PipelineSchema().load(
                        json.load(pipeline_json))
                    if errors:
                        return ErrorCodeAndMessageAdditionalDetails(
                            UNEXPECTED_ERROR, errors)
                    else:
                        response.append(pipeline)
    if pipeline_property:
        response = [i for i in response if pipeline_property in i.properties]
        if property_value:
            response = [
                i for i in response
                if property_value == i.properties[pipeline_property]
            ]
    if pipeline_identifier:
        response = [i for i in response if pipeline_identifier == i.identifier]
    return response


def get_all_pipelines(_type: str = None) -> list:
    if not _type:
        pipeline_directory = app.config['PIPELINE_DIRECTORY']
    else:
        pipeline_directory = os.path.join(app.config['PIPELINE_DIRECTORY'],
                                          _type)

    all_pipelines = [
        f for f in scandir(pipeline_directory)
        if not f.name.startswith(".") and f.is_file()
    ]
    return all_pipelines


def get_pipeline(pipeline_identifier: str,
                 only_path: bool = False) -> Pipeline:
    all_pipelines = get_all_pipelines()

    for pipeline in all_pipelines:
        with open(pipeline.path) as f:
            try:
                pipeline_json = json.load(f)
                if pipeline_json["identifier"] == pipeline_identifier:
                    return pipeline if only_path else PipelineSchema().load(
                        pipeline_json).data
            except json.JSONDecodeError:
                # We log the invalid pipeline, but just continue instead of crashing
                logger = logging.getLogger('server-error')
                logger.error("Invalid pipeline at {}".format(pipeline.path))

    return None


def export_all_pipelines() -> (bool, str):
    for descriptor_type in SUPPORTED_DESCRIPTORS:
        all_pipelines = get_all_pipelines(descriptor_type)

        for pipeline in all_pipelines:
            carmin_pipeline = os.path.join(app.config['PIPELINE_DIRECTORY'],
                                           "{}_{}".format(
                                               descriptor_type, pipeline.name))

            descriptor = Descriptor.descriptor_factory_from_type(
                descriptor_type)
            export, error = descriptor.export(pipeline.path, carmin_pipeline)
            if error:
                return False, error
    return True, None


def get_original_descriptor_path_and_type(
        pipeline_identifier: str) -> ((str, str), ErrorCodeAndMessage):

    carmin_descriptor_path = get_pipeline(pipeline_identifier, True)

    if not carmin_descriptor_path:
        return (None, None), INVALID_PIPELINE_IDENTIFIER

    descriptor_type = carmin_descriptor_path.name[:carmin_descriptor_path.name.
                                                  index("_")]
    original_descriptor_filename = carmin_descriptor_path.name[
        carmin_descriptor_path.name.index("_") + 1:]
    original_descriptor_path = os.path.join(app.config['PIPELINE_DIRECTORY'],
                                            descriptor_type,
                                            original_descriptor_filename)
    return (original_descriptor_path, descriptor_type), None


def get_descriptor_json(pipeline_path: str) -> (any, ErrorCodeAndMessage):
    try:
        with open(pipeline_path) as f:
            pipeline_json = json.load(f)
            return pipeline_json, None
    except OSError:
        return None, PATH_DOES_NOT_EXIST
