__title__ = "Svelte Django Dockerized"
__author__ = "Jody Doolittle"

import os, sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, os.path.join(BASE_DIR, ""))

VERSION = 0.1

SITE_ID = 1

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

SERVER_TYPE = os.environ.get("SERVER_TYPE")

DEBUG = int(os.environ.get("DJANGO_DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

ENABLE_USERNAMES = bool(os.environ.get("DJANGO_ENABLE_USERNAMES", default=False))

CACHE_BACKEND = os.environ.get(
    "DJANGO_CACHE_BACKEND", default="django_redis.cache.RedisCache"
)

CACHE_HOST = os.environ.get("DJANGO_CACHE_HOST", default="redis")

CACHE_KEY_PREFIX = os.environ.get("DJANGO_CACHE_KEY_PREFIX", default="")

CACHE_DEFAULT_TIMEOUT = os.environ.get("DJANGO_CACHE_DEFAULT_TIMEOUT", default=300)

SQL_HOST = os.environ.get("SQL_HOST", default="postgres")

SQL_PORT = os.environ.get("SQL_PORT", default="5432")

SQL_DATABASE = os.environ.get("SQL_DATABASE", default="postgres")

SQL_USER = os.environ.get("SQL_USER", default="postgres")

SQL_PASSWORD = os.environ.get("SQL_PASSWORD", default="postgres")

SQL_ENGINE = os.environ.get(
    "DJANGO_SQL_ENGINE", default="django.db.backends.postgresql"
)
