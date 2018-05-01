"""Usage: carmin-server run [options]

Launches the server

Options:
    -p <port>, --port <port>  The server will listen on this port
    -c, --container           Launch the server inside a Docker container
    """

import json
from subprocess import call
from pathlib import Path
from docopt import docopt

from cli_helper import project_root


def config_dict():
    root_dir = Path(__file__).resolve().parent.parent
    config_file = Path(root_dir, 'CONFIG.json')
    try:
        with open(config_file) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except TypeError:
        return {}


CONFIG = config_dict()

if __name__ == '__main__':
    args = docopt(__doc__)
    port = args.get('--port') or '8080'
    try:
        port = int(port)
    except ValueError:
        print("Invalid port number. Port must be an integer.")
        exit(1)
    if args.get('--container'):
        call(['docker', 'build', '-t=carmin-server', '..'])
        call([
            'docker', 'run', '-p', '{}:8080'.format(port), '-e',
            'DATABASE_URI="sqlite:////carmin-db/app.db"', '-v',
            '{}:/carmin-assets/pipelines'.format(
                CONFIG.get('PIPELINE_DIRECTORY')),
            '-v', '{}:/carmin-assets/data'.format(
                CONFIG.get('DATA_DIRECTORY')), 'carmin-server'
        ])
    else:
        call(['python3', '-m', 'server', str(port)], cwd=project_root())
