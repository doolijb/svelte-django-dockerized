__title__ = "Svelte Django Dockerized"
__author__ = "Jody Doolittle"

import os
import sys
from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent

sys.path.insert(0, os.path.join(BASE_DIR, ""))

VERSION: float = 0.1

SITE_ID = 1

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY: str | None = os.environ.get("DJANGO_SECRET_KEY")

if SECRET_KEY is None:
    raise ValueError("DJANGO_SECRET_KEY must be set")

SERVER_TYPE: str = os.environ.get("SERVER_TYPE", "dev")

DEBUG: int = int(os.environ.get("DJANGO_DEBUG", default=0))

ALLOWED_HOSTS: list[str] = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

ENABLE_USERNAMES: bool = bool(os.environ.get("DJANGO_ENABLE_USERNAMES", default=True))

CACHE_BACKEND: str = os.environ.get(
    "DJANGO_CACHE_BACKEND", default="django.core.cache.backends.redis.RedisCache"
)

CACHALOT_ENABLED: bool = bool(os.environ.get("DJANGO_CACHALOT_ENABLED", default=True))

CACHE_HOST: str = os.environ.get("DJANGO_CACHE_HOST")

CACHE_KEY_PREFIX: str = os.environ.get("DJANGO_CACHE_KEY_PREFIX", default="")

CACHE_DEFAULT_TIMEOUT: int = int(
    os.environ.get("DJANGO_CACHE_DEFAULT_TIMEOUT", default=300)
)

CACHALOT_TIMEOUT: int = int(
    os.environ.get("DJANGO_CACHALOT_TIMEOUT", default=CACHE_DEFAULT_TIMEOUT)
)

LOG_LEVEL: str = os.environ.get("DJANGO_LOG_LEVEL")

SQL_HOST: str = os.environ.get("DJANGO_SQL_HOST")

SQL_PORT: str = os.environ.get("DJANGO_SQL_PORT")

SQL_DATABASE: str = os.environ.get("DJANGO_SQL_DATABASE")

SQL_USER: str = os.environ.get("DJANGO_SQL_USER")

SQL_PASSWORD: str = os.environ.get("DJANGO_SQL_PASSWORD")

SQL_ENGINE: str = os.environ.get(
    "DJANGO_SQL_ENGINE", default="django.db.backends.postgresql"
)

# If not secret key is set, raise an error and provide a new one with instructions
if SECRET_KEY is None:
    new_key = os.urandom(32)
    raise ValueError(
        f"""
    `DJANGO_SECRET_KEY` must be set in .env file!
    Set a key and re up the container.
    Here is a new key you can use:
    {new_key}\n
    """
    )
