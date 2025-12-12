web: gunicorn mi_tienda.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A mi_tienda worker --loglevel=info