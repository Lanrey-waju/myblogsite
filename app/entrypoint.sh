#!/bin/sh

if [ "$DATABASE" = "postgres"]
then

    while ! nc -z db-dev 5432; do
        echo "Waiting for postgres"
        sleep 0.1
    done

    echo "Postgresql Started"
fi

# python manage.py flush --no-input
python manage.py migrate --no-input


exec "$@"