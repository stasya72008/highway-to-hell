FROM tiangolo/uwsgi-nginx-flask:python2.7

ENV LISTEN_PORT 8080
EXPOSE 8080

ENV UWSGI_INI /web_app/uwsgi.ini

COPY ./web_app /web_app

WORKDIR /web_app
