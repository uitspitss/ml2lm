FROM python:3.7

RUN apt-get update -y && apt-get install -y nginx supervisor less && \
rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN pip3 install uwsgi
RUN mkdir -p /var/log/uwsgi /var/log/nginx /var/www/code
WORKDIR /var/www/code
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY docker-components/nginx/nginx.conf /etc/nginx/sites-enabled/default
COPY docker-components/nginx/nginx-supervisor.conf  /etc/supervisor/conf.d/
COPY docker-components/uwsgi/uwsgi-supervisor.conf  /etc/supervisor/conf.d/
