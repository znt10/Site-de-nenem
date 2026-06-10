#!/bin/sh
set -e

mkdir -p "${DATA_DIR:-/app}/media/produtos"

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py create_minio_bucket

if [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py shell -c "
from django.contrib.auth.models import User
email = '$DJANGO_SUPERUSER_EMAIL'
password = '$DJANGO_SUPERUSER_PASSWORD'
if not User.objects.filter(username=email).exists():
    User.objects.create_superuser(username=email, email=email, password=password)
    print('Superusuario criado:', email)
else:
    print('Superusuario ja existe:', email)
"
fi

exec "$@"
