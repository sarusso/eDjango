import os

# Django imports
from django.core.exceptions import ImproperlyConfigured

# eDjango imports
from edjango.common.utils import discover_apps
from edjango.common.utils import booleanize

#===============================
#  Base settings
#===============================

# Quick-start development and prototyping settings - unsuitable for real production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#k%566hw@w%1((_&=640_4w#p)piwt$m4%#(9x^+it5(h1b6zy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = booleanize(os.environ.get('DJANGO_DEBUG', False))

# SECURITY WARNING: check if you want this in production
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

# Middleware
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

# Urls config
ROOT_URLCONF = 'edjango.urls'

# Static files (Django will look for a 'static' dir in every App and serve properly)
# Read more: https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'

# Templates
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

# Wsgi
WSGI_APPLICATION = 'edjango.wsgi.application'


#===============================
#  Databases
#===============================

# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

default_db_engine = 'django.db.backends.sqlite3'
default_db_name   = os.path.join(BASE_DIR, '../db-edjango.sqlite3')
if not os.environ.get('DJANGO_DB_NAME'):
    print('\nSETTINGS WARNING: I will use the default DB! -> {}\n'.format(default_db_name))

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


#===============================
#  Internationalization
#===============================

# Read more:https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#===============================
#  Project settings
#===============================

EDJANGO_PROJECT_NAME = os.environ.get('EDJANGO_PROJECT_NAME', 'eDjango Project')
EDJANGO_PUBLIC_HTTP_HOST = os.environ.get('EDJANGO_PUBLIC_HTTP_HOST', 'http://localhost:8080')

EDJANGO_EMAIL_SERVICE = os.environ.get('EDJANGO_EMAIL_SERVICE', 'Sendgrid')
if not EDJANGO_EMAIL_SERVICE in ['Sendgrid', None]:
    raise ImproperlyConfigured('Invalid EDJANGO_EMAIL_METHOD ("{}")'.format(EDJANGO_EMAIL_SERVICE))
EDJANGO_EMAIL_FROM = os.environ.get('EDJANGO_EMAIL_FROM', 'ejango project <info@edjango.project>')
EDJANGO_EMAIL_APIKEY = os.environ.get('EDJANGO_EMAIL_APIKEY', None)


#===============================
#  Logging
#===============================

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
        #    'propagate': False,
        #},
        'edjango': {
            'handlers': ['console'], #['mail_admins'],
            'level': EDJANGO_LOG_LEVEL,
            'propagate': False, # Do not propagate or the root logger will emit as well, and even at lower levels. 
        },
        'django': {
            'handlers': ['console'], #['mail_admins'],
            'level': DJANGO_LOG_LEVEL,
            'propagate': False, # Do not propagate or the root logger will emit as well, and even at lower levels. 
        }, 
        # Read more about the 'django' logger: https://docs.djangoproject.com/en/1.11/topics/logging/#django-logger
        # Read more about logging in the right way: https://lincolnloop.com/blog/django-logging-right-way/
    }
}


