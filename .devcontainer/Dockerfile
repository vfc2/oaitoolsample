FROM python:3.12-bullseye AS base_image

# System update and install dependencies
RUN apt-get update && \
    apt-get -y install unzip && \
    apt-get -y install curl && \
    apt-get -y install gnupg && \
    apt-get -y install wget

# Azure SQL ODBC Driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    ACCEPT_EULA=Y apt-get install -y mssql-tools18 && \
    echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc && \
    apt-get install -y unixodbc-dev && \
    apt-get install -y libgssapi-krb5-2

ENV PATH="$PATH:/opt/mssql-tools18/bin"