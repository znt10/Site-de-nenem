#!/bin/sh
set -e

mkdir -p "${DATA_DIR:-/app}/media/produtos"

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py create_minio_bucket || true

if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py shell -c "
from django.contrib.auth.models import User
username = 'admin'
password = '$DJANGO_SUPERUSER_PASSWORD'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email='', password=password)
    print('Superusuario criado:', username)
else:
    print('Superusuario ja existe:', username)
"
fi

exec "$@"
