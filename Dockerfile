FROM tiangolo/uwsgi-nginx-flask:python2.7

ENV LISTEN_PORT 8080
EXPOSE 8080

ENV UWSGI_INI /rest/uwsgi.ini

COPY ./rest /rest

WORKDIR /rest
