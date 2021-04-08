#!/bin/sh

set -e

# if it is the first time to run the container
if [ $INIT_DB -eq 1 && ! -f /initialised ]; then # change to 0 when you don't want to initialise db
  python manage.py flush --no-input #flush destroys db
  python manage.py makemigrations
  python manage.py migrate
  python manage.py collectstatic --noinput --clear
  echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('em',
                      'gu53jut@mytum.de', 'gu53jut')" | python manage.py shell
  touch /initialised
fi

# python manage.py runserver 0.0.0.0:8000

# uwsgi --socket :8000 --master --enable-threads --module cnv_proj/cnv_proj.wsgi

gunicorn cnv_proj.wsgi -b 0.0.0.0:8000 --timeout 600000