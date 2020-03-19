FROM python:3.7-buster
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    nano libsasl2-dev python3-dev zlib1g-dev python3-pydot \
    libldap2-dev libssl-dev netcat ca-certificates \
    xterm net-tools build-essential python-dev automake libpq-dev \
    binutils libproj-dev gdal-bin \
    autoconf gettext && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
ADD ./src/requirements.txt /code/

WORKDIR /code
RUN pip install -r requirements.txt

