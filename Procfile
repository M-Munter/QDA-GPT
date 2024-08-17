web: daphne -b 0.0.0.0 -p $PORT mysite.asgi:application
worker: python manage.py runworker analysis_channel
release: python manage.py migrate && python create_users.py


