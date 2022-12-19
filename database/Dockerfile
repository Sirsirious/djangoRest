FROM postgres:15.1

RUN apt-get update \
    && apt-get install wget -y \
    && apt-get install postgresql-15-postgis-3 -y \
    && apt-get install postgis -y \
    && apt install postgresql-contrib -y

COPY ./db.sql /docker-entrypoint-initdb.d/