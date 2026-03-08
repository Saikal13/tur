#!/usr/bin/env bash
# Выход при ошибке
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate