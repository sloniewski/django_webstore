import os

BASE_DIR = os.path.dirname(os.path.realpath(os.path.dirname(__file__) + "/.."))

SECRET_KEY = '02cc5x8u+-rga7)3&al^cepc6-g=qy^$yq+%$4_uq9(nltp4lf'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'webstore.users',
    'webstore.product',
    'webstore.cart',
    'webstore.order',
    'webstore.core',
    'webstore.delivery',
    'webstore.payment',

    'dashboard.main',
    'dashboard.product_panel',
    'dashboard.delivery_panel',
    'dashboard.order_panel',
    'dashboard.payment_panel',
    'dashboard.users_panel',

    'django.contrib.admindocs',
    'django.forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'webstore.core.context_processors.cart_info',
                'webstore.core.context_processors.categories',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/webstore/'

AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_URL = '/users/login'

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert card deep-purple',
    messages.INFO: 'alert card blue white-text',
    messages.SUCCESS: 'alert card green white-text',
    messages.WARNING: 'alert card yellow',
    messages.ERROR: 'alert card red white-text',
}

MEDIA_URL = 'files/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'webstore/core/media')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST_USER = 'placeholder@test.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}