release: python manage.py migrate
release: python manage.py collectstatic
web: gunicorn mysite.wsgi --log-file -