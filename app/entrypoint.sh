#!bin/sh

if [ "$DATABASE" = "postgres"]
then
    echo "Waiting for postgres"

    while !mc -z $SQL_HOST $SQLP_PORT; do
        sleep 0.1
    done

    echo "Postgresql Started"
fi

python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"