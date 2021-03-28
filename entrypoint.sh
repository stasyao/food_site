#!/bin/sh 
 
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py loaddata fixtures.json
python manage.py thumbnail cleanup
python manage.py thumbnail clear

gunicorn config.wsgi -b 0.0.0.0:8000