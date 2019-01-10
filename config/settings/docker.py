from .base import *

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

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

BROKER_URL = 'redis://redis_cache:6379'
CELERY_BROKER_URL = 'redis://redis_cache:6379'
CELERY_RESULT_BACKEND = 'redis://redis_cache:6379'
CELERY_TASK_RESULT_EXPIRES = 60*60
DJANGO_SETTINGS_MODULE = 'config.settings.local'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
