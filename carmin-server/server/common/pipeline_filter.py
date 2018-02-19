import os
import json
from server import app
from server.resources.models.pipeline import Pipeline, PipelineSchema


def pipelines(pipeline_identifier: str = None,
              study_identifier: str = None,
              pipeline_property: str = None,
              property_value: str = None):
    response = []
    pipeline_path = app.config['PIPELINE_DIRECTORY']
    for subdir, dirs, files in os.walk(pipeline_path):
        if study_identifier:
            dirs[:] = [i for i in dirs if i == study_identifier]
        for file in files:
            real_path = os.path.realpath(os.path.join(subdir, file))
            if file.endswith(".json"):
                with open(real_path) as pipeline_json:
                    pipeline, errors = PipelineSchema().load(
                        json.load(pipeline_json))
                    if errors:
                        print(errors)
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
