#!/usr/bin/env python3
"""CARMIN-Server

A lightweight server for the execution of remote pipelines.

Usage:
    carmin-server [--help] [--version] COMMAND [OPTIONS...]

Options:
    -h, --help     Print help page and quit
    -v, --version  Print version information and quit

Commands:
    setup  Install and configure the server
    run    Launch the server
    """

from subprocess import call
from pathlib import Path
from docopt import docopt
from cli_helper import project_root


def get_version():
    root_path = project_root()
    version_file = open(Path(root_path, 'VERSION'))
    return version_file.read().strip()


if __name__ == '__main__':
    args = docopt(__doc__, options_first=True, version=get_version())

    argv = [args['COMMAND']] + args['OPTIONS']

    if args['COMMAND'] == 'setup':
        import carmin_server_setup
        try:
            exit(call(['python3', 'carmin_server_setup.py'] + argv))
        except KeyboardInterrupt:
            exit()
    elif args['COMMAND'] == 'run':
        import carmin_server_run
        try:
            exit(call(['python3', 'carmin_server_run.py'] + argv))
        except KeyboardInterrupt:
            pass
    elif args['COMMAND'] in ['help', None]:
        exit(call(['python3', 'carmin_server.py', '--help']))
    else:
        exit("{} is not a carmin-server command. See 'carmin-server --help.'".
             format(args['COMMAND']))
