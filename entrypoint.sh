#!/bin/sh

echo "Waiting for database..."

python - << END
from core.wait_for_db import wait_for_db
wait_for_db()
END

echo "Database ready!"

python manage.py migrate

exec supervisord -c deploy/supervisord.conf
