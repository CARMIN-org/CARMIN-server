FROM python:3.6.4

WORKDIR /carmin

COPY . /carmin

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV SERVER_PORT 80

EXPOSE $SERVER_PORT

CMD ["python", "server.py"]
