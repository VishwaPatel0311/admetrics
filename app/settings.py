import os

DB_NAME = os.getenv('DB_NAME', "admetrics2")
DB_USER = os.getenv('DB_USER', "newuser")
DB_PASSWORD = os.getenv('DB_PASSWORD', "mypass")
DB_PORT = os.getenv('DB_PORT', "5432")
DB_HOST = os.getenv('DB_HOST', "localhost")
WEB_PORT = int(os.getenv('WEB_PORT', 14011))



DB_CONNECTION = "{}:{}@{}:{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

print(f"{DB_CONNECTION=}")

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")