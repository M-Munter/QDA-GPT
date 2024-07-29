release: python manage.py collectstatic --noinput
web: gunicorn mysite.wsgi --timeout 600 --log-file -
worker: celery -A mysite worker --loglevel=info