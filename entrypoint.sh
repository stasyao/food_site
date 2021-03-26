#!/bin/sh 
 
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py loaddata fixtures.json

gunicorn config.wsgi -b 0.0.0.0:8000