#!/usr/bin/env bash
# build.sh

# install dependencies
pip install -r requirements.txt

# collect static files
python manage.py collectstatic --noinput

# apply migrations
python manage.py migrate

# inkwell_api/createsuperuser.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inkwell_api.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("pat", "pattee13@gmail.com", "changeme123")
    print("Superuser created.")
else:
    print("Superuser already exists.")
