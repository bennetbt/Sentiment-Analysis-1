FROM postgres:15

ENV POSTGRES_USER=pgsqldev4
ENV POSTGRES_PASSWORD=enter
ENV POSTGRES_DB=Sentimental_Analysis

COPY init.sql /docker-entrypoint-initdb.d/
