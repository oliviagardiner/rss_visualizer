FROM debian:bookworm

RUN apt-get update && apt-get install -y \
    build-essential libssl-dev libffi-dev python3-dev \
    cron \
    python3 \
    python3-pip \
    python-is-python3 && \
    mkdir /app && \
    apt-get clean

COPY crontab /etc/crontab

RUN chmod 0644 /etc/crontab

WORKDIR /app