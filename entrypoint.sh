#!/bin/sh

if [ "$POSTGRES_DB" = "pawnshop" ]
then
    echo "Waiting for postgres..."
    echo $POSTGRES_HOST 
    echo $POSTGRES_PORT

    while ! nc -zv $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi


python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
pytest -vvv
python manage.py runserver 0.0.0.0:8000

exec "$@"
