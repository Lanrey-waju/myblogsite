#!/bin/sh

if [ "$DAABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQLP_PORT; do
        slwwp 0.1
    done

    echo "Postgres started"
fi

exec "$@"