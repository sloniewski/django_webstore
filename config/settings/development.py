import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.realpath(os.path.dirname(__file__) + "/.."))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '02cc5x8u+-rga7)3&al^cepc6-g=qy^$yq+%$4_uq9(nltp4lf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'webstore',
        'USER': 'db_user',
        'PASSWORD': 'super_secret',
        'HOST': 'postgres_db',
        'PORT': '5432',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis_cache:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "webstore",
    }
}

MEDIA_URL = 'files/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'webstore/core/media')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST_USER = 'placeholder@test.com'

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
