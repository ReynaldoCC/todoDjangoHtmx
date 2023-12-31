###########
# BUILDER #
###########

# pull official base image
FROM python:3.11-slim-bullseye as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# lint
RUN pip install --upgrade pip
RUN pip install flake8==6.0.0
COPY . /usr/src/app/
RUN flake8 --ignore=E501 .

# install python dependencies
COPY ./requirements* ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.11-slim-bullseye

# create directory for the app user
RUN mkdir -p /home/todo_app

# create the app user
RUN addgroup --system todo_app && adduser --system --group todo_app

# create the appropriate directories
ENV HOME=/home/todo_app
ENV APP_HOME=/home/todo_app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements* ./
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R todo_app:todo_app $APP_HOME

# change to the app user
USER todo_app
