# CARMIN Server

[![Build Status](https://travis-ci.org/simon-dube/CARMIN-server.svg?branch=develop)](https://travis-ci.org/simon-dube/CARMIN-server)
[![Coverage Status](https://coveralls.io/repos/github/simon-dube/CARMIN-server/badge.svg?branch=develop)](https://coveralls.io/github/simon-dube/CARMIN-server?branch=develop)

CARMIN-server is a lightweight server implementation of the [CARMIN API](https://app.swaggerhub.com/apis/CARMIN/carmin-common_api_for_research_medical_imaging_network/0.3)

## Table of Contents

- [Installation](#installation)
  - [Installing Locally](#installing-locally)
  - [Installing with Docker](#installing-with-docker)
- [Usage](#usage)
  - [Authentication](#authentication)
  - [Uploading Data to the Server](#uploading-data-to-the-server)
  - [Getting Data from the Server](#getting-data-from-the-server)
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

By default, `CARMIN-server` uses a lightweight `sqlite` database that does not require any setup. `CARMIN-server` also natively supports a `postgres` database. If you'd like to use an external `postgres` database, simply set a `$DATABASE_URL` environment variable to point to the production database URL.
```bash
$ export DATABASE_URL=postgresql://user:password@localhost/carmin
```

### Installing Locally

To install and run the server locally, execute the following command from the root directory:
```bash
$ pip install .
$ python -m server
# If you are getting exceptions when running pip install, make sure that your
# virtualenv is configured.
# You can also run the command with sudo, although this is not recommended.
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

## Usage

CARMIN-server automatically creates an admin user with `admin` as username and password.

You can get your `apiKey` by authenticating into the system:

### Authentication
```bash
## /authenticate
curl -X "POST" "http://localhost:8080/authenticate" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d $'{
  "username": "admin",
  "password": "admin"
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

### Uploading Data to the Server
Let's add some data to the server with the `PUT /path/{completePath}` method:

```bash
## /path/{completePath}
curl -X "PUT" "http://localhost:8080/path/admin/hello_world.txt" \
     -H 'apiKey: [secret_api_key]' \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d $'{
  "type": "File",
  "base64Content": "aGVsbG8gd29ybGQK"
}'## /path/{completePath}
```

The server should reply with a `201: Created` code, indicating that the resource was successfully
uploaded to the server.

### Getting Data from the Server

Now we can query the server to see if our file really exists:

```bash
## /path/{completePath}
curl "http://localhost:8080/path/admin/hello_world.txt?action=properties" \
     -H 'apiKey: [secret_api_key]'
```

The server should return a `Path` object, which describes the resource that we uploaded:

```json
{
  "platformPath": "http://localhost:8080/path/admin/hello_world.txt",
  "lastModificationDate": 1521740108,
  "isDirectory": false,
  "size": 12,
  "mimeType": "text/plain"
}
```

## CARMIN API Specification

For a complete description of the server functionality, please refer to the [CARMIN API Specification](https://app.swaggerhub.com/apis/CARMIN/carmin-common_api_for_research_medical_imaging_network/0.3)
