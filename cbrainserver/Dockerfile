FROM python:3.6.4

WORKDIR /carmin

COPY . /carmin

RUN pip install --trusted-host pypi.python.org .

ENV SERVER_PORT 80
ENV COVERALLS_REPO_TOKEN ljhyghrf22rJ9bWfiDT3jVr7E85ruP7i0

EXPOSE $SERVER_PORT

CMD ["python", "carmin_cbrain/server.py"]
