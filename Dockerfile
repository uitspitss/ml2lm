FROM python:3.7

RUN apt-get update -y && apt-get install -y less && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
CMD ["uwsgi", "--http", ":8081", "-y", "docker-components/uwsgi/uwsgi.yml"]
