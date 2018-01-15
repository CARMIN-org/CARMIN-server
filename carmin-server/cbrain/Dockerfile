FROM python:3.6.4

WORKDIR /carmin-server/cbrain

COPY . /carmin-server/cbrain

RUN pip install --trusted-host pypi.python.org .

ENV SERVER_PORT 80

EXPOSE $SERVER_PORT

CMD ["python", "server.py"]
