import os
import json
from server.resources.models.execution import Execution


def write_inputs_to_file(execution: Execution, path_to_execution_dir: str):
    inputs_json_file = os.path.join(path_to_execution_dir, 'inputs.json')
    write_content = json.dumps(execution.input_values)
    with open(inputs_json_file, 'w') as f:
        f.write(write_content)
