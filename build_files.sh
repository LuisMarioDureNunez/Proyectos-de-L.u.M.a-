#!/bin/bash

# Build script para Vercel
echo "BUILD START"

# Instalar dependencias
python3.9 -m pip install -r requirements.txt

# Collectstatic
python3.9 manage.py collectstatic --noinput --clear

echo "BUILD END"