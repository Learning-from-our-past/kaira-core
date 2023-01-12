FROM python:3.6-stretch
WORKDIR /app
COPY requirements.txt /app
RUN apt-get update && apt-get -y install libffi-dev libxslt-dev libc-dev libfuzzy-dev && \
    pip install -r requirements.txt
CMD ["tail", "-f", "/dev/null"]

