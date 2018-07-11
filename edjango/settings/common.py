"""
Django settings for edjango project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from edjango.common.utils import discover_apps
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#k%566hw@w%1((_&=640_4w#p)piwt$m4%#(9x^+it5(h1b6zy'

# SECURITY WARNING: don't run with debug turned on in production!
from edjango.common.utils import booleanize
DEBUG = booleanize(os.environ.get('DJANGO_DEBUG', False))

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

# Apps auto discovery
INSTALLED_APPS = INSTALLED_APPS + discover_apps(BASE_DIR)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'edjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Django will look for a 'templates' dir in every app and render properly
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'edjango.wsgi.application'


#---------------------
# Databases
#---------------------

# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

default_db_engine = 'django.db.backends.sqlite3'
default_db_name   = os.path.join(BASE_DIR, '../db-edjango.sqlite3')
if not os.environ.get('DJANGO_DB_NAME'):
    print '\nSETTINGS WARNING: I will use the default DB! -> {}\n'.format(default_db_name)

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DJANGO_DB_ENGINE', default_db_engine),
        'NAME': os.environ.get('DJANGO_DB_NAME', default_db_name),
        'USER': os.environ.get('DJANGO_DB_USER', None),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', None),
        'HOST': os.environ.get('DJANGO_DB_HOST', None),
        'PORT': os.environ.get('DJANGO_DB_PORT',None),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# Django will look for a 'static' dir in evry app and serve properly
STATIC_URL = '/static/'

#===============================
# Project settings
#===============================

EDJANGO_PROJECT_NAME = os.environ.get('EDJANGO_PROJECT_NAME', 'eDjango Project')
EDJANGO_PUBLIC_HTTP_HOST = os.environ.get('EDJANGO_PUBLIC_HTTP_HOST', 'http://localhost:8080')

EDJANGO_EMAIL_METHOD = os.environ.get('EDJANGO_EMAIL_METHOD', 'Sendgrid')
if not EDJANGO_EMAIL_METHOD in ['Sendgrid', None]:
    raise ImproperlyConfigured('Invalid EDJANGO_EMAIL_METHOD ("{}")'.format(EDJANGO_EMAIL_METHOD))
EDJANGO_EMAIL_FROM = os.environ.get('EDJANGO_EMAIL_FROM', 'ejango project <info@edjango.project>')
EDJANGO_EMAIL_APIKEY = os.environ.get('EDJANGO_EMAIL_APIKEY', None)


# ------------------------------
#    Logging
# ------------------------------

DJANGO_LOG_LEVEL = os.environ.get('DJANGO_LOG_LEVEL','ERROR')
EDJANGO_LOG_LEVEL = os.environ.get('EDJANGO_LOG_LEVEL','ERROR')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
 
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s',
        },
        'halfverbose': {
            'format': '%(asctime)s, %(name)s: [%(levelname)s] - %(message)s',
            'datefmt': '%m/%d/%Y %I:%M:%S %p'
        }
    },
 
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
 
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'halfverbose',
        },
    },
 
    'loggers': {
        #'django.request': {
        #    'handlers': ['console'], #['mail_admins'],
        #    'level': DJANGO_LOG_LEVEL,
        #    'propagate': True,
        #},
        'edjango': {
            'handlers': ['console'], #['mail_admins'],
            'level': EDJANGO_LOG_LEVEL,
            'propagate': True,
        },
        'django': {
            'handlers': ['console'], #['mail_admins'],
            'level': DJANGO_LOG_LEVEL,
            'propagate': True,
        }, 
    }
}

RAISE_EXCEPTIONS = False

