web: daphne -b 0.0.0.0 -p $PORT mysite.asgi:application
worker: python manage.py runworker analysis_channel
release: python create_users.py


