#!/usr/bin/env bash
# start-server.sh
cd cnv_app
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    python manage.py createsuperuser --no-input
fi

#uwsgi --http :8000 --wsgi-file cnv_app.wsgi --master --processes 4 --threads 2
# gunicorn cnv_app.wsgi:application --bind 0.0.0.0:8000 --timeout 172800 #--user www-data --bind 0.0.0.0:8010 --workers 3
gunicorn cnv_app.wsgi:application -b :8000 --timeout 600000 --workers=4 --worker-class=gevent --threads=3 --worker-connections=1000
