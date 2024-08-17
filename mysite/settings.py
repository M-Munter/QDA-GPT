"""
Django settings for the 'mysite' project.

This script contains the configuration settings for the Django project.
It includes settings for installed apps, middleware, databases,
static files, templates, and other configurations.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information, see:
https://docs.djangoproject.com/en/5.0/topics/settings/
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from a .env file
load_dotenv()

# Define the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load sensitive information and configurations from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-+^3va&8@w%(og5gl596@yrvt7l6x3scf2f0yk(7#v2ia!gy$!l')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Redis URL for Django Channels (used for WebSockets and background tasks)
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')

# AWS S3 Settings
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'


# Define the hosts allowed to serve the project
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'qda-gpt-11509cd6d17d.herokuapp.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',  # Django Channels for handling WebSockets
    'qda_gpt',  # Custom application for the project
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL and WSGI/ASGI application configuration
ROOT_URLCONF = 'mysite.urls'
WSGI_APPLICATION = 'mysite.wsgi.application'
ASGI_APPLICATION = 'mysite.asgi.application'

# Template engine configuration
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
            ],
        },
    },
]


# Custom environment variable to control specific behavior (set manually if needed)
HEROKU_CUSTOM = os.getenv('HEROKU', False)

# Database configuration (different for Heroku and local environments)
if HEROKU_CUSTOM:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default='postgres://localhost')
    }
else:  # Local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Detect if the app is running on Heroku (based on the presence of the 'DYNO' environment variable)
ON_HEROKU = 'DYNO' in os.environ

# Redis configuration for Django Channels (used for WebSockets and background tasks)
if ON_HEROKU:
    # Heroku Redis configuration
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [{
                    "address": os.getenv('REDIS_URL'),
                    "ssl_cert_reqs": None  # Disable SSL certificate verification on Heroku
                }],
            },
        },
    }
else:
    # Local Redis configuration
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')],  # Use local Redis without SSL
            },
        },
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and media files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Media Files with S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirect to the dashboard after login
LOGIN_REDIRECT_URL = 'dashboard'

# Django-Heroku configuration (applies additional settings when on Heroku)
if os.getenv('HEROKU', False):
    import django_heroku
    django_heroku.settings(locals())

# Logging configuration for debugging and error tracking
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

import logging

# Basic logging setup to output logs to the console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# CSRF trusted origins (add Heroku domain to trusted list)
CSRF_TRUSTED_ORIGINS = [
    'https://qda-gpt-11509cd6d17d.herokuapp.com',
]



