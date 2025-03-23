#!/bin/sh
set -e

echo "Applying migrations..."
python manage.py migrate

echo "Creating superuser or skipping..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

User.objects.filter(username=username).exists() or \
    User.objects.create_superuser(username, email, password)
EOF

exec python manage.py runserver 0.0.0.0:8000