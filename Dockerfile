FROM python:3.11-slim-buster

LABEL maintainer="Victor Goh"

# Install OS dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
        && rm -rf /var/lib/apt/lists/*

# Install latest pip version
RUN pip install --upgrade pip

# Create directory for dbt config
RUN mkdir -p /root/.dbt

# Install Airflow
ARG AIRFLOW_VERSION=2.6.1

RUN pip install apache-airflow==${AIRFLOW_VERSION}

COPY requirements.txt /tmp/

# Install dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

ENV AIRFLOW_HOME=/opt/airflow

WORKDIR $AIRFLOW_HOME

# Initialise Airflow Database
RUN airflow db init

RUN airflow users create \
    --username victorwkb \
    --firstname Victor \
    --lastname Goh \
    --role Admin \
    --email victorwkb@gmail.com \
    --use-random-password

COPY dags/ $AIRFLOW_HOME/dags/

