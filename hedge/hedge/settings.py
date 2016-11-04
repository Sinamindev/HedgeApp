"""
Django settings for hedge project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
import json
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Secret information: (loaded below with DB secrets)
SECRET_KEY = ""
EMAIL_HOST = ""
EMAIL_HOST_USER = ""
DEFAULT_FROM_EMAIL = ""
EMAIL_HOST_PASSWORD = ""

# Non-secret:
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_EMAIL_SUBJECT_PREFIX = '[Hedge Registration] '
SEND_ACTIVATION_EMAIL = True
REGISTRATION_AUTO_LOGIN = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
SITE_ID = 1
ADMINS = (('Phil', 'phillipwstewart@gmail.com'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Necessary if DEBUG is False. should be restricted to the host address and name,
# but can be defined as ['*'] to accept any hostnames (not recommended)
ALLOWED_HOSTS = ['.hedgeapp.co']

# Application definition
INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sites',
	'huey.djhuey',
	'registration',
	'splash',
	'portfolio',
	'stocks',
	'leaderboard',
	'account',
	'common',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.gzip.GZipMiddleware',
	'htmlmin.middleware.HtmlMinifyMiddleware',
	'htmlmin.middleware.MarkRequestMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.security.SecurityMiddleware',
)

HUEY = {
	'backend': 'huey.backends.redis_backend',
	'name': 'huey tasks',
	'connection': {'host': 'localhost', 'port': 6667},
	'always_eager': False,
	'consumer_options': {'workers': 1},
}

HTML_MINIFY = True
ROOT_URLCONF = 'hedge.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'common.context_processors.is_mobile',
				'common.context_processors.ticker',
			],
		},
	},
]

WSGI_APPLICATION = 'hedge.wsgi.application'

# Playing around with this...
LOG_FILE = os.path.join(BASE_DIR, 'runserver.log')

# Database
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': '',
		'USER': '',
		'PASSWORD': '',
		'HOST': '',
		'PORT': '',
		#'ATOMIC_REQUESTS' : True,
	}
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '/var/tmp/django_default_cache.sock',
        'TIMEOUT': 60
    },
    "prices" : {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '/var/tmp/django_prices_cache.sock',
        'TIMEOUT': 60
    },
	"quotes" : {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '/var/tmp/django_quotes_cache.sock',
        'TIMEOUT': 120
    },
	"hot_stocks" : {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '/var/tmp/django_hots_cache.sock',
        'TIMEOUT': 3600
    },
	"ticker_symbols" : {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '/var/tmp/django_ticker_cache.sock',
        'TIMEOUT': 900
    }
}

# Load secret info:
with open('secrets.json', 'r') as f:
	secrets = json.loads(f.read())
	SECRET_KEY = secrets['SECRET_KEY']
	EMAIL_HOST = secrets['EMAIL_HOST']
	EMAIL_HOST_USER = secrets['EMAIL_HOST_USER']
	DEFAULT_FROM_EMAIL = secrets['DEFAULT_FROM_EMAIL']
	SERVER_EMAIL = secrets['DEFAULT_FROM_EMAIL']
	EMAIL_HOST_PASSWORD = secrets['EMAIL_HOST_PASSWORD']
	d = DATABASES['default']
	SECRET_KEY = secrets['SECRET_KEY']
	d['NAME'] = secrets['DATABASE_NAME']
	d['HOST'] = secrets['DATABASE_HOST']
	d['PORT'] = secrets['DATABASE_PORT']
	d['USER'] = secrets['DATABASE_USER']
	d['PASSWORD'] = secrets['DATABASE_PASSWORD']

SYMBOLS = []
with open('valid_symbols.txt', 'r') as f:
	for line in f:
		SYMBOLS.append(line.strip())
SYMBOLS = frozenset(SYMBOLS)


time_str = '[{}] '.format(datetime.utcnow())
with open('logs/settings_load.log', 'a') as f:
	f.write(time_str + ' settings.py reloaded.\n')

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = ()
if DEBUG:
	STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static2'),)

