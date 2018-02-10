release: python manage.py migrate
release: python manage.py collectstatic --noinput
web: gunicorn --env DJANGO_SETTINGS_MODULE=mysite.settings mysite.wsgi --log-file -