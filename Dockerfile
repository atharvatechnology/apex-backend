FROM python:3.10.4 as builder

# setting the workdir
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install gcc -y \
    && apt-get clean

# install dependencies
RUN pip install --upgrade pip
RUN pip install flake8
RUN flake8 --ignore=E501,F401 .


COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

COPY . .

FROM python:3.10.4-slim

RUN mkdir -p /home/app

# RUN addgroup app && adduser app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

RUN apt-get update
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY . $APP_HOME

RUN chmod 777 $APP_HOME/entrypoint.sh

ENTRYPOINT ["/home/app/web/entrypoint.sh"]
