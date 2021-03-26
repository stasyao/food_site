FROM python:3.9-alpine 
 
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONBUFFERED 1 
 
WORKDIR /code 
COPY Pipfile Pipfile.lock /code/ 
RUN apk update && apk add --no-cache --virtual .build-deps ca-certificates gcc postgresql-dev python3-dev linux-headers musl-dev libffi-dev jpeg-dev zlib-dev && pip install pipenv && pipenv install --system
 
COPY . /code 
 
ENTRYPOINT sh ./entrypoint.sh