import os
from boutiques import bosh
from jsonschema import ValidationError
from server import app
from server.resources.models.descriptor.descriptor_abstract import Descriptor


class Boutiques(Descriptor):
    @classmethod
    def validate(cls, descriptor_path, input_path):
        try:
            bosh(["invocation", descriptor_path, "-i", input_path])
        except ValidationError as e:
            return False, e.message
        return True, None

    @classmethod
    def export(cls, input_descriptor_path, output_descriptor_path):
        relative_path = os.path.relpath(
            output_descriptor_path, start=app.config['PIPELINE_DIRECTORY'])
        try:
            bosh([
                "export", "carmin", input_descriptor_path, "--identifier",
                relative_path, output_descriptor_path
            ])
        except Exception:
            return False, "Boutiques descriptor at '{}' is invalid and could not be translated. Please fix it before launching the server.".format(
                input_descriptor_path)

        if not os.path.exists(output_descriptor_path):
            return False, "Boutiques descriptor at '{}' was exported without error, but no output file was created."
        return True, None

    @classmethod
    def execute(cls, user_data_dir, descriptor, input_data):
        return [
            "bosh", "exec", "launch", "-v{0}:{0}".format(user_data_dir),
            descriptor, input_data
        ]
