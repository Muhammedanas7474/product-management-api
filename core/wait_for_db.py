import time

import psycopg2
from django.conf import settings


def wait_for_db():
    db = settings.DATABASES["default"]
    while True:
        try:
            conn = psycopg2.connect(
                dbname=db["NAME"],
                user=db["USER"],
                password=db["PASSWORD"],
                host=db["HOST"],
                port=db["PORT"],
            )
            conn.close()
            break
        except psycopg2.OperationalError:
            print("Database unavailable, waiting 2 seconds...")
            time.sleep(2)
