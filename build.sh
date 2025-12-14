#!/usr/bin/env bash
# build.sh para Render
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Solo ejecuta migraciones si es la primera vez
python manage.py migrate --noinput

# Recolecta archivos estáticos
python manage.py collectstatic --noinput
