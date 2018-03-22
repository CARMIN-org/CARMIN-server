# CARMIN Server

[![Build Status](https://travis-ci.org/simon-dube/CARMIN-server.svg?branch=develop)](https://travis-ci.org/simon-dube/CARMIN-server)
[![Coverage Status](https://coveralls.io/repos/github/simon-dube/CARMIN-server/badge.svg?branch=develop)](https://coveralls.io/github/simon-dube/CARMIN-server?branch=develop)

## Installation

To run the server, execute the following command from the root directory:
```
$ pip3 install .
$ python3 -m server
```

By default, the server will be running on port 8080.

Test that the server is running by executing the following command:

```
$ curl http://localhost:8080/platform
```

### Using with Docker

To run carmin-server in a Docker container, execute the following command, again from the root directory:

```
docker build -t=carmin-server .
docker run -p 8080:8080 \
		   -v $PIPELINE_DIRECTORY:/carmin-assets/pipelines \
		   -v $DATA_DIRECTORY:/carmin-assets/data \
		   carmin-server
```

### Important Environment Variables

Before launching the server, environment variables must point to both the Pipeline directory and the Data directory. The pathname must be absolute.
```
$ # In a UNIX environment
$ export PIPELINE_DIRECTORY=/path/to/pipelines
$ export DATA_DIRECTORY=/path/to/data

> # In a Windows environment
> set PIPELINE_DIRECTORY=C:\path\to\pipelines
> set DATA_DIRECTORY=C:\path\to\data
```

Pipelines can be organized by `study` as follows:
```
/path/to/data/and/pipelines

├── data
└── pipelines
    ├── study1
    │   ├── pipeline1.json
    │   └── pipeline2.json
    └── study2
        └── pipeline3.json
```

## Usage
