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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#k%566hw@w%1((_&=640_4w#p)piwt$m4%#(9x^+it5(h1b6zy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
        'django.request': {
            'handlers': ['console'], #['mail_admins'],
            'level': DJANGO_LOG_LEVEL,
            'propagate': True,
        },
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



# ####################################################################
# From old environment.py
# ####################################################################

# ----------------------------------------
#    Static/Media files
# ----------------------------------------

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_PATH = os.path.join(PROJECT_PATH, 'static')
# MEDIA_ROOT = os.environ.get('MEDIA_ROOT', os.path.join(PROJECT_PATH, 'media'))
# MEDIA_URL = '/media/'
# 
# STATICFILES_DIRS = (
#     STATIC_PATH,
# )

#if not booleanize(os.environ.get('REST_DEBUG', False)):
#REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ('rest_framework.renderers.JSONRenderer',)

# ####################################################################
# Old common.py
# ####################################################################

# 
# 
# """
# Django settings for main project.
# 
# For more information on this file, see
# https://docs.djangoproject.com/en/1.6/topics/settings/
# 
# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/1.6/ref/settings/
# """
# 
# # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# import os
# 
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# SETTINGS_DIR = os.path.dirname(__file__)  # current directory
# 
# PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)  # directory up by one (project folder)
# PROJECT_PATH = os.path.abspath(PROJECT_PATH)  # project directory in abs form
# 
# # TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
# 
# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
# 
# SECRET_KEY = '&18db$%mj)_xg9$qa*l6npnl#w!6%3nu4k0i6y@2(0h-54&pl4'
# 
# TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
# 
# TEMPLATE_DIRS = (
#     # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
#     # Don't forget to use absolute paths, not relative paths.
#     TEMPLATE_PATH,
# )
# 
# ALLOWED_HOSTS = []
# 
# 
# INSTALLED_APPS = (
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'django.contrib.sites',
#     'rest_framework',
#     'rest_framework.authtoken',
#     'corsheaders',
#     'allauth',
#     'allauth.account',
#     'rest_auth.registration',
#     'edjango.webapp',
#     'south',
#     'mathfilters',
# )
# 
# MIDDLEWARE_CLASSES = (
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.common.CommonMiddleware',)
# 
# if os.environ.get('DISABLE_CSRF') not in ('True', '1'):
#     MIDDLEWARE_CLASSES += (
#         'django.middleware.csrf.CsrfViewMiddleware',
#     )
# 
# MIDDLEWARE_CLASSES += (
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# )
# 
# ROOT_URLCONF = 'edjango.urls'
# 
# WSGI_APPLICATION = 'edjango.wsgi.application'
# 
# 
# # Internationalization
# # https://docs.djangoproject.com/en/1.6/topics/i18n/
# 
# LANGUAGE_CODE = 'en-us'
# 
# TIME_ZONE = 'UTC'
# 
# USE_I18N = True
# 
# USE_L10N = True
# 
# USE_TZ = True
# 
# AUTHENTICATION_BACKENDS = (
#     # Needed to login by username in Django admin, regardless of `allauth`
#     "django.contrib.auth.backends.ModelBackend",
# 
#     # `allauth` specific authentication methods, such as login by e-mail
#     "allauth.account.auth_backends.AuthenticationBackend",
# )
# 
# AUTH_USER_MODULE = 'django.contrib.auth.models.User'
# 
# # ------------------------------
# #    Rest
# # ------------------------------
# REST_FRAMEWORK = {
#     'PAGINATE_BY': 10,
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         ('rest_framework.authentication.SessionAuthentication' if os.environ.get('DISABLE_CSRF') not in (
#             'True', '1') else 'edjango.auth.authentication.NoCSRFSessionAuthentication',
#          'rest_framework.authentication.BasicAuthentication')
#     ),
#     # Disallow automatic forms in API documentation, that sometimes break
#     # things because they are a little too invasive in ApiView introspection
#     'FORM_METHOD_OVERRIDE': None,
# }
# 
# # ------------------------------
# #    Cors
# # ------------------------------
# CORS_ORIGIN_WHITELIST = (
#     'localhost',
#     '127.0.0.1',
# )
# 
# CORS_ALLOW_CREDENTIALS = True
# 
