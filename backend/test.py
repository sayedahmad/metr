from os import environ

from backend.settings import *

TEST = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "metr",
        "USER": "admin",
        "PASSWORD": "secret",
        "HOST": "localhost",
        "PORT": "",
    }
}


# DEBUGGING

DEBUG = True


# SECURITY

ALLOWED_HOSTS = [
    ".localhost",
    "127.0.0.1",
    "[::1]",
]