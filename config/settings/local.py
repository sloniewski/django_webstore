from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'webstore',
        'USER': 'db_user',
        'PASSWORD': 'super_secret',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# CELERY_BROKER_URL = 'amqp://localhost'
DJANGO_SETTINGS_MODULE = 'config.settings.local'
# celery -A config  worker -l info