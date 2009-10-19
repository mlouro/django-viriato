# -*- coding: utf-8 -*-
import os
PROJECT_ROOT = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(PROJECT_ROOT)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS   = ()
MANAGERS = ADMINS

DATABASE_ENGINE     = 'sqlite3'
DATABASE_NAME       = 'dev.db'
DATABASE_USER       = ''
DATABASE_PASSWORD   = ''
DATABASE_HOST       = ''
DATABASE_PORT       = ''

TIME_ZONE = 'Europe/Lisbon'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = os.path.join('static')
MEDIA_URL  = '/static/'

STATIC_ROOT = os.path.join('static')
STATIC_URL  = '/static/'

ADMIN_MEDIA_PREFIX = '/media/'


SECRET_KEY = 'pm_&n6+ols+16a=*t9yl6g@d0txx=6bj=_iw8pq2&4dz27)bss'


EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
MAIL_TO = ''


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.request',
    'core.context_processors.static_url',
)


ugettext = lambda s: s
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = '/admin/'


ROOT_URLCONF = 'viriato.urls'


TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'core',
    'projects',
    'django_vcs',
    'contact',
    'contract',
    'receipt',
    'company',
    'newsletter',
    'invoices',
)

try:
    from local_settings import *
except ImportError:
    import sys
    sys.stderr.write("local_settings.py not set; using default settings\n")
