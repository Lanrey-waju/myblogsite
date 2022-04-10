#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then

    while ! nc -z blog-db 5432; do
        echo "Waiting for postgres..."
        sleep 0.1
    done

    echo "Postgres started"
fi

python manage.py migrate --no-input
python manage.py collectstatic

exec "$@"
