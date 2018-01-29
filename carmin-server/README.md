# CARMIN-CBRAIN Server Implementation

[![Build Status](https://travis-ci.org/louis-ver/CARMIN.svg?branch=develop)](https://travis-ci.org/louis-ver/CARMIN)
[![Coverage Status](https://coveralls.io/repos/github/louis-ver/CARMIN/badge.svg?branch=setup-py)](https://coveralls.io/github/louis-ver/CARMIN?branch=setup-py)

## Installation

To run the server, execute the following command from the `/carmin-server/cbrain` directory:
```
$ pip3 install .
$ python3 -m server
```

By default, the server will be running on port 8080.

Test that the server is running by executing the following command:

```
$ curl http://localhost:8080/platform/
```

### Using with Docker

To run carmin-server in a Docker container, execute the following command, again from the root directory:

```
$ docker build -t carmin-server .
$ docker run -p 8080:8080 carmin-server
```

## Usage
