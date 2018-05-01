"""Usage: carmin-server setup [options]

Options:
    -p <path>, --pipeline-directory <path>  Specify path for pipeline directory
    -d <path>, --data-directory <path>      Specify path for data directory
    -w <path>, --database <path>            Specify path for database

"""

import json
from pathlib import Path
from docopt import docopt


def is_interactive(invocation_list):
    return not (invocation_list.get('--database')
                and invocation_list.get('--pipeline-directory')
                and invocation_list.get('--data-directory'))


def write_to_config_file(config):
    root_dir = Path(__file__).resolve().parent.parent
    config_file = Path(root_dir, 'CONFIG.json')
    with open(config_file, 'w') as f:
        json.dump(config, f)


def print_install_banner():
    width = 50
    delimiter = '-' * width
    print('{0}\nCARMIN-Server Setup (Press CTRL-C to quit)\n{0}'.format(
        delimiter))


ask_pipeline = "Enter path to pipeline directory: "
ask_data = "Enter path to data directory: "
ask_database = "Enter path or URI to the database (to use the default sqlite database, leave blank): "

if __name__ == '__main__':
    args = docopt(__doc__)
    try:
        if is_interactive(args):
            print_install_banner()
            step_count = 1
            if not args.get('--pipeline-directory'):
                pipeline_path = input('{}. {}'.format(step_count,
                                                      ask_pipeline))
                step_count += 1
            if not args.get('--data-directory'):
                data_path = input('{}. {}'.format(step_count, ask_data))
                step_count += 1
            if not args.get('--database'):
                database_path = input('{}. {}'.format(step_count,
                                                      ask_database))
            config_dict = {
                "PIPELINE_DIRECTORY": pipeline_path,
                "DATA_DIRECTORY": data_path,
                "DATABASE_URL": database_path
            }
            write_to_config_file(config_dict)
        exit("\nCARMIN-Server was successfully configured.")
    except KeyboardInterrupt:
        exit()
