FROM python:3.6.4

RUN mkdir -p /carmin-server/cbrain
WORKDIR /carmin-server/cbrain

COPY . /carmin-server/cbrain

RUN pip3 install --no-cache-dir --trusted-host pypi.python.org .

ENV SERVER_PORT 80

EXPOSE $SERVER_PORT

ENTRYPOINT ["python3"]

CMD ["-m", "server"]
