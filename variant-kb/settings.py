import os
# import django_heroku
from os.path import dirname, join, realpath

import dj_database_url
import dj_email_url
import dotenv as env

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']
SECRET_KEY = '0r%dj0ub-l26q=m#tpa$jfi5=21a)4a*m&^hc7@ki@n0^#ipo)'

# Set environment variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# TODO: smtps is depreciated use submission?
env.load_dotenv(os.path.join(BASE_DIR, '.env'))

# Application definition
INSTALLED_APPS = [
    'api.apps.ApiConfig',
    'side.apps.SideConfig',
    'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_tables2',
    'rest_framework',
    'mathfilters',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'variant-kb.urls'
DATETIME_FORMAT = DATE_FORMAT = os.getenv('DATE_FORMAT', 'N j, Y')

# User & Email Settings
AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = '/'
EMAIL = {
    'default': dj_email_url.config(default=os.getenv('SENDGRID_URL', 'smtps://irene.chae@uhn.ca:scMN4244scMN4244@smtp.sendgrid.net:587')),
}
# EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_API_KEY', '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')


# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.getenv('BASE_DIR', ''), 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }
]
WSGI_APPLICATION = 'variant-kb.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL', 'mysql://root:password@localhost:3306/variant_db')),
}
DEFAULT_AUTO_FIELD='django.db.models.AutoField'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'en-us')

TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = '/staticfiles/'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(os.getenv('BASE_DIR', ''), 'static'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Upload Settings
UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')

FILE_UPLOAD_MAX_MEMORY_SIZE = 5000000
FILE_UPLOAD_TEMP_DIR = join(dirname(realpath(__file__)), 'static/tmp-uploads/')
FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler'
)
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000

# django_heroku.settings(locals())
