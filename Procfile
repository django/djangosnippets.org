#web: gunicorn -b 0.0.0.0:$PORT -k gevent -w 4 djangosnippets.wsgi:application
web: python manage.py runserver 0.0.0.0:$PORT
