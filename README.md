# CARMIN Server

[![Build Status](https://travis-ci.org/simon-dube/CARMIN-server.svg?branch=develop)](https://travis-ci.org/simon-dube/CARMIN-server)
[![Coverage Status](https://coveralls.io/repos/github/simon-dube/CARMIN-server/badge.svg?branch=develop)](https://coveralls.io/github/simon-dube/CARMIN-server?branch=develop)

CARMIN-server is a lightweight server implementation of the [CARMIN API](https://app.swaggerhub.com/apis/CARMIN/carmin-common_api_for_research_medical_imaging_network/0.3)

## Table of Contents

- [Installation](#installation)
  - [Database](#database)
  - [Installing Locally](#installing-locally)
  - [Installing with Docker](#installing-with-docker)
  - [Common Installation Problems](#common-installation-problems)
  	  - [pg_config](#pg_config)
- [Usage](#usage)
  - [Authentication](#authentication)
  	  - [Creating Accounts](#creating-accounts)
  	  - [Changing Your Password](#changing-your-password)
  - [Uploading Data to the Server](#uploading-data-to-the-server)
  - [Getting Data from the Server](#getting-data-from-the-server)
  - [Adding a Pipeline](#adding-a-pipeline)
  - [Creating and Launching an Execution](#creating-and-launching-an-execution)
- [CARMIN API Specification](#carmin-api-specification)

## Installation

Before launching the server, environment variables must point to both the Pipeline directory and the Data directory. The pathname must be absolute.
```bash
$ # In a UNIX environment
$ export PIPELINE_DIRECTORY=/path/to/pipelines
$ export DATA_DIRECTORY=/path/to/data

> # In a Windows environment
> set PIPELINE_DIRECTORY=C:\path\to\pipelines
> set DATA_DIRECTORY=C:\path\to\data
```

For now, `CARMIN-server` only supports boutiques descriptors for pipelines. Your boutiques descriptors
must be placed inside a `boutiques` directory, as such:
```
└── pipelines
    └── boutiques
        ├── pipeline_descriptor_1.json
        └── pipeline_descriptor_2.json
```

### Database

By default, `CARMIN-server` uses a lightweight `sqlite` database that does not require any setup. `CARMIN-server` also natively supports a `postgres` database. If you'd like to use an external `postgres` database, simply set a `$DATABASE_URI` environment variable to point to the production database URL.
```bash
$ export DATABASE_URI=postgresql://user:password@localhost/carmin
```

### Installing Locally

To install and run the server locally, execute the following command from the root directory:
```bash
$ pip install .
$ python -m server
# If you are getting exceptions when running pip install, make sure that your
# virtualenv is configured.
# You can also run the command with the --user flag.
```

By default, the server will be running on port 8080.

Test that the server is running by executing the following command:

```bash
$ curl http://localhost:8080/platform
```

### Installing with Docker

To run carmin-server in a Docker container, execute the following command, again from the root directory:

```bash
docker build -t=carmin-server .
docker run -p 8080:8080 \
		   -v $PIPELINE_DIRECTORY:/carmin-assets/pipelines \
		   -v $DATA_DIRECTORY:/carmin-assets/data \
		   carmin-server
```

### Common Installation Problems

#### pg_config

The server launch might fail due to a missing `pg_config` installation on the computer. To fix this, download `libpq-dev` using your distro's package manager. (On Red Hat and derived distributions, install `postgresql-devel`)

## Usage

CARMIN-server automatically creates an admin user with `admin` as username. The password is printed to the console upon launching the server for the first time.

You can get your `apiKey` by authenticating into the system:

### Authentication
```bash
curl -X "POST" "http://localhost:8080/authenticate" \
     -d $'{
  "username": "admin",
  "password": "[default-admin-password]"
}'

```

This request returns a `json` object containing the `apiKey` that will be required
for authenticated queries.

```json
{
  "httpHeader": "apiKey",
  "httpHeaderValue": "[secret-api-key]"
}
```

In subsequent requests, all we have to do is include the `apiKey` in the headers.

#### Creating Accounts

To add new users to the database, an admin must send a `POST` request at the `/users/register` endpoint. The admin must include both `username` and `password` in the request body.

Example:
```
curl -X "POST" "http://localhost:8080/users/register" \
     -H 'apiKey: [secret-api-key]' \
     -d $'{
  "username": "new-user",
  "password": "user-password"
}'
```

#### Changing Your Password

Passwords can be changed by sending a `POST` request to the `/users/edit` endpoint.
Admins can change passwords for any user, and regular users can only change their own. To change a user's password, an admin must include both the `username` and `password` in the request body. For a user to change his/her own password, only the `password` is required.

Example (Admin):
```
curl -X "POST" "http://localhost:8080/users/edit" \
     -H 'apiKey: [secret-admin-api-key]' \
     -d $'{
  "username": "some-user",
  "password": "new-password"
}'
```

Example (Regular User):
```
curl -X "POST" "http://localhost:8080/users/edit" \
     -H 'apiKey: [secret-api-key]' \
     -d $'{
  "password": "new-password"
}'
```

### Uploading Data to the Server
Let's add some data to the server with the `PUT /path/{completePath}` method:

```bash
curl -X "PUT" "http://localhost:8080/path/admin/new_user.txt" \
     -H 'apiKey: [secret-api-key]' \
     -d $'{
  "type": "File",
  "base64Content": "bmV3IENBUk1JTiB1c2VyCg=="
}'
```

The server should reply with a `201: Created` code, indicating that the resource was successfully
uploaded to the server.

### Getting Data from the Server

Now we can query the server to see if our file really exists:

```bash
curl "http://localhost:8080/path/admin/new_user.txt?action=properties" \
     -H 'apiKey: [secret-api-key]'
```

The server should return a `Path` object, which describes the resource that we uploaded:

```json
{
  "platformPath": "http://localhost:8080/path/admin/new_user.txt",
  "lastModificationDate": 1521740108,
  "isDirectory": false,
  "size": 12,
  "mimeType": "text/plain"
}
```

To see what the file contains, we can issue the same request, but replace the action
with `content`:

```bash
curl "http://localhost:8080/path/admin/new_user.txt?action=content" \
     -H 'apiKey: [secret-api-key]'
```

### Adding a pipeline

Without pipelines to execute, the server is not very useful. Let's change that.

Pipelines can be added to `CARMIN-server` simply by adding them to the directory at `PIPELINE_DIRECTORY`.
`CARMIN-server` supports [the boutiques schema](https://github.com/boutiques/boutiques) for its descriptors.

Thankfully, we have one handy to help you test out your server. `output.json` simply takes a file,
and copies the contents of the file to another file, just like the `cp` UNIX command.

Add this descriptor file in `$PIPELINE_DIRECTORY/boutiques`:
```json
{
    "command-line": "echo \"Welcome to CARMIN-Server, $(cat [INPUT_FILE]).\" &> [OUTPUT_FILE]",
    "container-image": {
        "image": "alpine",
        "type": "docker"
    },
    "description": "A simple script to test output files",
    "error-codes": [
        {
            "code": 2,
            "description": "File does not exist."
        }
    ],
    "inputs": [
        {
            "id": "input_file",
            "name": "Input file",
            "optional": false,
            "type": "File",
            "value-key": "[INPUT_FILE]"
        }
    ],
    "invocation-schema": {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "additionalProperties": false,
        "dependencies": {},
        "description": "Invocation schema for output.",
        "properties": {
            "input_file": {
                "type": "string"
            }
        },
        "required": [
            "input_file"
        ],
        "title": "output.invocationSchema",
        "type": "object"
    },
    "name": "output",
    "output-files": [
        {
            "id": "output_file",
            "name": "Output file",
            "path-template": "./greeting.txt",
            "path-template-stripped-extensions": [
                ".txt",
                ".mnc",
                ".cpp",
                ".m",
                ".j"
            ],
            "value-key": "[OUTPUT_FILE]"
        }
    ],
    "schema-version": "0.5",
    "tool-version": "1.0"
}

```

You will need to restart the server for the translation from Boutiques to CARMIN to happen.

Once that's done, issue a `GET /pipelines` request:

```bash
curl "http://localhost:8080/pipelines" \
     -H 'apikey: [secret-api-key]'

```

We should see `output.json`, translated in CARMIN format:
```json
[
  {
    "identifier": "[pipeline-identifier]",
    "name": "output",
    "version": "1.0",
    "description": "A simple script to test output files",
    "canExecute": true,
    "parameters": [
      {
        "id": "input_file",
        "name": "Input file",
        "type": "File",
        "isOptional": false,
        "isReturnedValue": false
      },
      {
        "id": "output_file",
        "name": "Output file",
        "type": "File",
        "isOptional": false,
        "isReturnedValue": true
      }
    ],
    "properties": {
      "boutiques": true
    },
    "errorCodesAndMessages": [
      {
        "errorCode": 2,
        "errorMessage": "File does not exist."
      }
    ]
  }
]
```

### Creating and Launching an Execution

We'd like to remotely execute this pipeline. To do this, we simply need to create an
execution, then launch it.

To create an execution, issue a `POST /executions` request, containing your input values:

```bash
curl -X "POST" "http://localhost:8080/executions" \
     -H 'apiKey: [secret-api-key]' \
     -d $'{
  "name": "my_first_execution",
  "pipelineIdentifier": "[pipeline-identifier]",
  "inputValues": {
    "input_file": "http://localhost:8080/path/admin/new_user.txt"
  }
}'

```

The server will then return a message, saying that the Execution was successfully created:

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 256
Server: Werkzeug/0.14.1 Python/3.6.4
Date: Tue, 27 Mar 2018 02:21:33 GMT

{
  "identifier": "[execution-identifier]",
  "name": "my_first_execution",
  "pipelineIdentifier": "[pipeline-identifier]",
  "status": "Initializing",
  "inputValues": {
    "input_file": "http://localhost:8080/path/admin/new_user.txt"
  }
}
```

We're ready to launch the execution:

```bash
curl -X "PUT" "http://localhost:8080/executions/[execution-identifier]/play" \
     -H 'apikey: [secret-api-key]' \
```

And that's it! The execution has been launched. To see the results of an execution,
simply look in `http://localhost:8080/path/admin/executions/[execution-identifier]`.

## CARMIN API Specification

For a complete description of the server functionality, please refer to the [CARMIN API Specification](https://app.swaggerhub.com/apis/CARMIN/carmin-common_api_for_research_medical_imaging_network/0.3)
