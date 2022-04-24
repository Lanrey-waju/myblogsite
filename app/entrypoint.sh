#!/bin/sh

# python manage.py flush --no-input
python manage.py migrate --no-input
python /usr/src/app/manage.py runserver 0.0.0.0:8000

