import os
basedir = os.path.abspath(os.path.dirname(__file__))

SUPPORTED_PROTOCOLS = ["http", "https", "ftp", "sftp", "ftps", "scp", "webdav"]

SUPPORTED_MODULES = [
    "Processing", "Data", "AdvancedData", "Management", "Commercial"
]


class Config(object):
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_DIRECTORY = os.environ.get('DATA_DIRECTORY')
    PIPELINE_DIRECTORY = os.environ.get('PIPELINE_DIRECTORY')


class ProductionConfig(Config):
    pass


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'test/database/app.db')
