#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py setup_default_user
daphne -b 0.0.0.0 -p 8000 config.asgi:application